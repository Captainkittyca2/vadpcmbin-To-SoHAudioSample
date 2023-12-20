# vadpcmbin-To-SoHAudioSample
## A tool to convert the vadpcm.bin files, created by z64audio.exe/z64rom, to the audio sample format that SoH, the Ocarina of Time PC Port , utilizes.

* Step 1: Open your wav file in audacity (audio editing tool) and modify the sample rate value to be the same as the sample rate of the audio you want to replace then go to `Effect->Pitch and Tempo->Change Speed and Pitch` and modify the speed value until it sounds approximately normal again. When exporting, make sure it's signed 16-bit float. Also, to check what's the sample rate of the audio you want to replace is, check the "Sounds" tab in [SoH Assets Guide](https://docs.google.com/spreadsheets/d/1rOTt_7Wr0OGfMR9tHom8dDOooM3rUocz9xi7axpR0sY/edit?usp=sharing)

* Step 2: Use [z64audio](https://github.com/z64tools/z64audio/releases/tag/2.2.0) or z64rom to convert your WAV file to vadpcm.bin. It should create two files which are a .vadpcm.bin file and a config.toml file. Both of these are important. You can ignore/delete the .book.bin file.

* Step 3: Use vadpcmToSample. When you first use the tool, it will open a pop-up screen and you need to select a voice/sfx SoH audio sample so the tool can acquire neccessary information. `(you can extract SoH audio samples using MPQ-Editor and opening oot.otr that SoH generates and navigating to audio/samples/ folder and extacting any of the voice/sfx sample files from there.)` After providing a SoH audio sample, the tool will create a `config.bruh` file in the same folder as the tool and will close itself. You shouldn't see that pop-up again when re-opening the tool.

* Step 4: Re-open vadpcmToSample and open the vadpcm.bin file (make sure the config.toml file is in the same folder as vadpcm.bin). The tool should automatically adjust the "loop start", "loop end", and "loop count" values to be same as the values that z64audio creates.

* Step 5: make a folder somewhere in your PC (for example, a folder called "myaudio") and then make a folder inside it and name it "audio" and make a folder inside "audio" folder called "samples". Then place your custom audio sample in the "samples" folder and rename it to the name of the audio sample you want to replace. Finally, using [retro](https://github.com/HarbourMasters64/retro), navigate to "Create OTR" -> "Custom" -> "Select Directory" and select the "myaudio" folder, then select "Stage Files" -> "Finalize OTR" -> "generate OTR" and place the otr file in the "mods" folder in soh. If you don't know the name of the audio sample you want to replace, use mpq-editor (google it) and open your oot.otr (or oot-mq.otr) and navigate to `audio/samples/` folder. There, you can see the names of all the audio samples for SoH.

## Note(s):
* The audio will very likely sound kinda glitchy even after adjusting the sample rate and speed value in audacity. At the moment i'm writing this, i still don't know what's the fix for this. The glitchy effects can be considered by some as somewhat minor though.

* Use SoH 8.0.3 or above.
