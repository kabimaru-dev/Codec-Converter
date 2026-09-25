import json
import os
from pathlib import Path
from ffmpeg import FFmpeg

input_file = input("Write name of the file(should be near with .py file): ")
output_file = "_experiment_video_"
compressed_times = 64
audio_bitrate="16000"
counter = 1
vformat = ".mkv"
acodec = "libopus"
target_bytes = Path(input_file).stat().st_size / compressed_times

ffprobe = (FFmpeg(executable="ffprobe").input(str(input_file),print_format="json",show_format=None,show_streams=None,))
media = json.loads(ffprobe.execute())
duration_seconds = float(media["format"]["duration"])

duration = duration_seconds
container_margin = 0.90
target_total_bitrate = (target_bytes * 8 / duration) * container_margin

def calculate(input_file, type="byte"):
    match type:
        case "byte":
            file = Path(input_file)
            size_bytes = file.stat().st_size
            return size_bytes
        case "kilobyte":
            file = Path(input_file)
            size_bytes = file.stat().st_size
            return size_bytes / 1024
        case "megabyte":
            file = Path(input_file)
            size_bytes = file.stat().st_size
            return size_bytes / 1024 / 1024
        case "gigabyte":
            file = Path(input_file)
            size_bytes = file.stat().st_size
            return size_bytes / 1024 / 1024 / 1024

def libaom_av1__experiment(input_file, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate):
    vcodec = "libaom-av1"
    output_file = str(counter) + output_file + vcodec + vformat

    print(input_file, "->", output_file)

    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(input_file)
        .output(
            output_file,

            map=[
                "0:v:0",
                "0:a?",
                "0:s?",
            ],

            **{
                "c:v": vcodec,
                "b:v": "0",
                "crf": "63",
                "cpu-used": "0",
                "row-mt": "1",
                "threads": "0",
                "pix_fmt": "yuv420p",

                "c:a": acodec,
                "b:a": audio_bitrate,
                "ac": "1",

                "c:s": "copy",

                "flush_packets": "1",
                "cluster_time_limit": "500",
                "cluster_size_limit": "16384",
                "f": "matroska",
            },
        )
    )

    ffmpeg.execute()

    print("original:", calculate(os.path.join(os.getcwd(), input_file), "megabyte"), "MB")
    print("   ", target_total_bitrate, "bitrate*")
    print("compressed:", calculate(os.path.join(os.getcwd(), output_file), "megabyte"), "MB")
    print("compressed times:", "x"+str(calculate(os.path.join(os.getcwd(), input_file), "byte")/calculate(os.path.join(os.getcwd(), output_file))))

    return output_file

def libvpx_vp9__experiment(input_file, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate):
    vcodec = "libvpx-vp9"
    output_file = str(counter) + output_file + vcodec + vformat
    
    print(input_file, "->", output_file)

    ffmpeg = (
        FFmpeg()
        .option("y")
        .option("hide_banner")
        .option("loglevel", "error")
        .input(input_file)
        .option("sn")
        .option("dn")
        .output(
            output_file,

            map=[
                "0:v:0",
                "0:a:0?",
            ],

            **{
                "b:v": target_total_bitrate,
                "c:v": vcodec,
                "force_key_frames": "expr:gte(t,n_forced*0.5)",
                "bf": "0",
                "flush_packets": "1",
                "muxdelay": "0",
                "max_interleave_delta": "0",
                "cluster_time_limit": "500",
                "cluster_size_limit": "16384",
                "c:a": acodec,
                "b:a": audio_bitrate,
                "deadline": "best",
                "cpu-used": "0",
            },
        )
    )

    counter += 1
    ffmpeg.execute()

    print("original:", calculate(os.path.join(os.getcwd(), input_file), "megabyte"), "MB")
    print("   ", target_total_bitrate, "bitrate*")
    print("compressed:", calculate(os.path.join(os.getcwd(), output_file), "megabyte"), "MB")
    print("compressed times:", "x"+str(calculate(os.path.join(os.getcwd(), input_file), "byte")/calculate(os.path.join(os.getcwd(), output_file))))

    return output_file

def libopenh264__experiment(input_file, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate):
    vcodec = "libopenh264"
    output_file = str(counter) + output_file + vcodec + vformat
    
    print(input_file, "->", output_file)

    ffmpeg = (
        FFmpeg()
        .option("y")
        .option("hide_banner")
        .option("loglevel", "error")
        .input(input_file)
        .option("sn")
        .option("dn")
        .output(
            output_file,

            map=[
                "0:v:0",
                "0:a:0?",
            ],

            **{
                "b:v": target_total_bitrate,
                "c:v": vcodec,
                "force_key_frames": "expr:gte(t,n_forced*0.5)",
                "bf": "0",
                "flush_packets": "1",
                "muxdelay": "0",
                "max_interleave_delta": "0",
                "cluster_time_limit": "500",
                "cluster_size_limit": "16384",
                "c:a": acodec,
                "b:a": audio_bitrate,
            },
        )
    )

    counter += 1
    ffmpeg.execute()

    print("original:", calculate(os.path.join(os.getcwd(), input_file), "megabyte"), "MB")
    print("   ", target_total_bitrate, "bitrate*")
    print("compressed:", calculate(os.path.join(os.getcwd(), output_file), "megabyte"), "MB")
    print("compressed times:", "x"+str(calculate(os.path.join(os.getcwd(), input_file), "byte")/calculate(os.path.join(os.getcwd(), output_file))))

    return output_file

def librav1e__experiment(input_file, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate):
    vcodec = "librav1e"
    output_file = str(counter) + output_file + vcodec + vformat
    
    print(input_file, "->", output_file)

    ffmpeg = (
        FFmpeg()
        .option("y")
        .option("hide_banner")
        .option("loglevel", "error")
        .input(input_file)
        .option("sn")
        .option("dn")
        .output(
            output_file,

            map=[
                "0:v:0",
                "0:a:0?",
            ],

            **{
                "b:v": target_total_bitrate,
                "c:v": vcodec,
                "force_key_frames": "expr:gte(t,n_forced*0.5)",
                "bf": "0",
                "flush_packets": "1",
                "muxdelay": "0",
                "max_interleave_delta": "0",
                "cluster_time_limit": "500",
                "cluster_size_limit": "16384",
                "c:a": acodec,
                "b:a": audio_bitrate,

                "speed": "10",
            },
        )
    )

    counter += 1
    ffmpeg.execute()

    print("original:", calculate(os.path.join(os.getcwd(), input_file), "megabyte"), "MB")
    print("   ", target_total_bitrate, "bitrate*")
    print("compressed:", calculate(os.path.join(os.getcwd(), output_file), "megabyte"), "MB")
    print("compressed times:", "x"+str(calculate(os.path.join(os.getcwd(), input_file), "byte")/calculate(os.path.join(os.getcwd(), output_file))))

    return output_file

def libx264__experiment(input_file, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate):
    vcodec = "libx264"
    output_file = str(counter) + output_file + vcodec + vformat
    
    print(input_file, "->", output_file)

    ffmpeg = (
        FFmpeg()
        .option("y")
        .option("hide_banner")
        .option("loglevel", "error")
        .input(input_file)
        .option("sn")
        .option("dn")
        .output(
            output_file,

            map=[
                "0:v:0",
                "0:a:0?",
            ],

            **{
                "b:v": target_total_bitrate,
                "c:v": vcodec,
                "force_key_frames": "expr:gte(t,n_forced*0.5)",
                "bf": "0",
                "flush_packets": "1",
                "muxdelay": "0",
                "max_interleave_delta": "0",
                "cluster_time_limit": "500",
                "cluster_size_limit": "16384",
                "c:a": acodec,
                "b:a": audio_bitrate,

                "preset": "veryslow",
            },
        )
    )

    counter += 1
    ffmpeg.execute()

    print("original:", calculate(os.path.join(os.getcwd(), input_file), "megabyte"), "MB")
    print("   ", target_total_bitrate, "bitrate*")
    print("compressed:", calculate(os.path.join(os.getcwd(), output_file), "megabyte"), "MB")
    print("compressed times:", "x"+str(calculate(os.path.join(os.getcwd(), input_file), "byte")/calculate(os.path.join(os.getcwd(), output_file))))

    return output_file

def libx265__experiment(input_file, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate):
    vcodec = "libx265"
    output_file = str(counter) + output_file + vcodec + vformat
    
    print(input_file, "->", output_file)

    ffmpeg = (
        FFmpeg()
        .option("y")
        .option("hide_banner")
        .option("loglevel", "error")
        .input(input_file)
        .option("sn")
        .option("dn")
        .output(
            output_file,

            map=[
                "0:v:0",
                "0:a:0?",
            ],

            **{
                "b:v": target_total_bitrate,
                "c:v": vcodec,
                "force_key_frames": "expr:gte(t,n_forced*0.5)",
                "bf": "0",
                "flush_packets": "1",
                "muxdelay": "0",
                "max_interleave_delta": "0",
                "cluster_time_limit": "500",
                "cluster_size_limit": "16384",
                "c:a": acodec,
                "b:a": audio_bitrate,

                "preset": "slow",
            },
        )
    )

    counter += 1
    ffmpeg.execute()

    print("original:", calculate(os.path.join(os.getcwd(), input_file), "megabyte"), "MB")
    print("   ", target_total_bitrate, "bitrate*")
    print("compressed:", calculate(os.path.join(os.getcwd(), output_file), "megabyte"), "MB")
    print("compressed times:", "x"+str(calculate(os.path.join(os.getcwd(), input_file), "byte")/calculate(os.path.join(os.getcwd(), output_file))))

    return output_file

# # 1
# result = libvpx_vp9__experiment(input_file, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate)

# # 2
# result = libaom_av1__experiment(result, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate)

# 3
# test__experiment(input_file, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate)

# # 3
# result = libaom_av1__experiment(input_file, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate)

# # 4
# result = libvpx_vp9__experiment(result, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate)

# # # # # # # # # 1
# result = libopenh264__experiment(input_file, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate)

# counter += 1  # 2
# librav1e__experiment(input_file, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate)

# counter += 1  # 3
# libx264__experiment(input_file, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate)

# counter += 1  # 4
# libx265__experiment(input_file, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate)



# counter += 1  # 5
# result = librav1e__experiment(result, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate)

# counter += 1  # 6
# result = libx264__experiment(result, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate)

# counter += 1  # 7
# result = libx265__experiment(result, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate)

# original: 8.80 MB
# compressed: 1.66 MB
# compressed times: x5.27

libopenh264__experiment(input_file, output_file, vformat, acodec, audio_bitrate, counter, target_total_bitrate)




















































    # ffmpeg -y \
    #     -hide_banner \
    #     -loglevel error \
    #     -i "$INPUT" \
    #     -map 0:v:0 \
    #     -map 0:a:0? \
    #     -sn \
    #     -dn \
    #     -c:v "$VCODEC" \
    #     "${VIDEO_ARGS[@]}" \
    #     "${EXTRA_ARGS[@]}" \
    #     -force_key_frames "expr:gte(t,n_forced*0.5)" \
    #     -bf 0 \
    #     -flush_packets 1 \
    #     -muxdelay 0 \
    #     -muxpreload 0 \
    #     -max_interleave_delta 0 \
    #     -cluster_time_limit 500 \
    #     -cluster_size_limit 16384 \
    #     -c:a libopus \
    #     -b:a "$AUDIO_BITRATE" \
    #     "$OUTPUT"