import argparse
import codecs
import os
import re
from datetime import datetime
from importlib.resources import files
from pathlib import Path

import numpy as np
import soundfile as sf
import tomli
from cached_path import cached_path
from omegaconf import OmegaConf

from f5_tts.infer.utils_infer import (
    mel_spec_type,
    target_rms,
    cross_fade_duration,
    nfe_step,
    cfg_strength,
    sway_sampling_coef,
    speed,
    fix_duration,
    infer_process,
    load_model,
    load_vocoder,
    preprocess_ref_audio_text,
    remove_silence_for_generated_wav,
)
from f5_tts.model import DiT, UNetT
from TTS.api import TTS


class F5Engine:
    def __init__(self):

        model = "F5-TTS"
        model_cfg = str(files("f5_tts").joinpath("configs/F5TTS_Base_train.yaml"))
        ckpt_file = ""
        vocab_file = ""

        self.ref_audio = "voices/hoang_03.wav"
        self.ref_text = "When the sunlight strikes raindrops in the air, they act as a prism and form a rainbow. The rainbow is a division of white light into many beautiful colors."

        self.save_chunk = False
        self.remove_silence = False
        load_vocoder_from_local = False

        self.vocoder_name = mel_spec_type
        self.target_rms = target_rms
        self.cross_fade_duration = cross_fade_duration
        self.nfe_step = 32 #nfe_step
        self.cfg_strength = cfg_strength
        self.sway_sampling_coef = sway_sampling_coef
        self.speed = 1.5 #speed
        self.fix_duration = fix_duration

        if self.save_chunk:
            output_chunk_dir = os.path.join(output_dir, f"{Path(output_file).stem}_chunks")
            if not os.path.exists(output_chunk_dir):
                os.makedirs(output_chunk_dir)


        # load vocoder
        if self.vocoder_name == "vocos":
            vocoder_local_path = "../checkpoints/vocos-mel-24khz"
        elif self.vocoder_name == "bigvgan":
            vocoder_local_path = "../checkpoints/bigvgan_v2_24khz_100band_256x"

        self.vocoder = load_vocoder(vocoder_name=self.vocoder_name, is_local=load_vocoder_from_local, local_path=vocoder_local_path)

        # load TTS model

        if model == "F5-TTS":
            model_cls = DiT
            model_cfg = OmegaConf.load(model_cfg).model.arch
            if not ckpt_file:  # path not specified, download from repo
                if self.vocoder_name == "vocos":
                    repo_name = "F5-TTS"
                    exp_name = "F5TTS_Base"
                    ckpt_step = 1200000
                    ckpt_file = str(cached_path(f"hf://SWivid/{repo_name}/{exp_name}/model_{ckpt_step}.safetensors"))
                    # ckpt_file = f"ckpts/{exp_name}/model_{ckpt_step}.pt"  # .pt | .safetensors; local path
                elif self.vocoder_name == "bigvgan":
                    repo_name = "F5-TTS"
                    exp_name = "F5TTS_Base_bigvgan"
                    ckpt_step = 1250000
                    ckpt_file = str(cached_path(f"hf://SWivid/{repo_name}/{exp_name}/model_{ckpt_step}.pt"))

        print(f"Using {model}...")
        self.ema_model = load_model(model_cls, model_cfg, ckpt_file, mel_spec_type=self.vocoder_name, vocab_file=vocab_file)
        self.isInitialised = False

    def initialise(self):
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        self.isInitialised = True

    def generate(self, gen_text, output_file):
        if not self.isInitialised:
            self.initialise()

        main_voice = {"ref_audio": self.ref_audio, "ref_text": self.ref_text}
        voices = {"main": main_voice}
        generated_audio_segments = []
        reg1 = r"(?=\[\w+\])"
        chunks = re.split(reg1, gen_text)
        reg2 = r"\[(\w+)\]"
        for text in chunks:
            if not text.strip():
                continue
            match = re.match(reg2, text)
            if match:
                voice = match[1]
            else:
                print("No voice tag found, using main.")
                voice = "main"
            if voice not in voices:
                print(f"Voice {voice} not found, using main.")
                voice = "main"
            text = re.sub(reg2, "", text)
            ref_audio_ = voices[voice]["ref_audio"]
            ref_text_ = voices[voice]["ref_text"]
            gen_text_ = text.strip()
            print(f"Voice: {voice}")
            audio_segment, final_sample_rate, spectragram = infer_process(
                ref_audio_,
                ref_text_,
                gen_text_,
                self.ema_model,
                self.vocoder,
                mel_spec_type=self.vocoder_name,
                target_rms=self.target_rms,
                cross_fade_duration=self.cross_fade_duration,
                nfe_step=self.nfe_step,
                cfg_strength=self.cfg_strength,
                sway_sampling_coef=self.sway_sampling_coef,
                speed=self.speed,
                fix_duration=self.fix_duration,
            )
            generated_audio_segments.append(audio_segment)

            if self.save_chunk:
                if len(gen_text_) > 200:
                    gen_text_ = gen_text_[:200] + " ... "
                sf.write(
                    os.path.join(output_chunk_dir, f"{len(generated_audio_segments)-1}_{gen_text_}.wav"),
                    audio_segment,
                    final_sample_rate,
                )

        if generated_audio_segments:
            final_wave = np.concatenate(generated_audio_segments)
            output_dir = os.path.dirname(output_file)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            with open(output_file, "wb") as f:
                sf.write(f.name, final_wave, final_sample_rate)
                # Remove silence
                if self.remove_silence:
                    remove_silence_for_generated_wav(f.name)
                print(f.name)


