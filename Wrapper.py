import sys
import torch

from main import load_data_setting
from main import load_model_decode

input_ori = sys.argv[1]
print(type(input_ori))
input = input_ori.decode("utf-8")
print(type(input))
f = open("./data/input", "w")
for each_word in list(input):
    f.write(each_word.encode("utf-8") + " O\n")
f.write("\n")
f.close()

data = load_data_setting("./data/my_saved_model.dset")
data.generate_instance_with_gaz("./data/input", 'raw')
decode_results = load_model_decode("./data/my_saved_model.2.model", data, 'raw', torch.cuda.is_available(), True)
data.write_decoded_results("./data/output", decode_results, 'raw')

f = open("./data/output", "r")
lines = f.readlines()


lines = [line for line in lines if len(line)>1]
all = []
result = ""
index = 0
print(len(lines))
while index != len(lines):
    if lines[index].decode("utf-8")[2] == u"B":
        tag = lines[index].decode("utf-8")[4:7]
        # print(tag)
        for j in range(index + 1, len(lines)):
            if lines[j].decode("utf-8")[2] == u"I":
                pass
            elif lines[j].decode("utf-8")[2] == u"O" or lines[j].decode("utf-8")[2] == u"B":
                index = j + 1
                break
            else:
                # print(str([index, j]))
                print(input_ori.decode("utf-8")[index:j+1].encode("utf-8"))
                # print(input.decode("utf-8")[index:j+1].encode("utf-8"))
                # print(input.decode("utf-8")[index:j+1].encode("utf-8"))
                all.append((tag, input_ori.decode("utf-8")[index:j+1].encode("utf-8")))
                result = result + input_ori.decode("utf-8")[index:j+1].encode("utf-8") + tag.encode("utf-8") + " "
                index = j + 1
                break
    else:
        index = index + 1
print(all)


# new_lines = []
# for line in lines:
#     if len(line) >= 2:
#         if line.decode("utf-8")[2] != "O":
#             new_lines.append(line[:-1])
# new_lines.append("   ")
# result = ""
# flag = None
# for index in range(len(new_lines)):
#     if flag != new_lines[index][-3:]:
#         if flag:
#             result = result + flag + " "
#         result = result + new_lines[index].decode("utf-8")[:1].encode("utf-8")
#         flag = new_lines[index][-3:]
#     else:
#         result = result + new_lines[index].decode("utf-8")[:1].encode("utf-8")
# result = result + "\n"
open("./data/output.format", "w").write(result+"\n")
print(result)
print("done")
