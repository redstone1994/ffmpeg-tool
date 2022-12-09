import ffmpeg

in_filename = "D:\MV.mp4"
out_filename = "D:\MV2.mp4"

width = 1920
height = 1080

process = (
    ffmpeg
    .input(in_filename)
    .output(out_filename)
    .overwrite_output()
    .global_args("-c:v", "h264_qsv")
    .run_async(pipe_stdout=True, pipe_stderr=True) #-hwaccel qsv
)
# out, err = process.communicate()

# print("err:"+err.decode("utf-8"))
# print("out:"+out.decode("utf-8"))

while True:
    err = process.stderr.read(100)
    if not err:
        print("==============")
        break

    print(err.decode("utf-8"))

process.wait()
