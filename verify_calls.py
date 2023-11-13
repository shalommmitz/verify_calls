import functools, os, pickle, glob
from deepdiff import DeepDiff

class Verify():
    def __init__(self, mode, folder):
        if mode not in ["RECORD", "VERIFY", "PLAY_BACK"]:
            print("ERROR: Mode paramter should be RECORD or VERIFY or PLAY_BACK - Aborting")
            exit()
        self.mode = mode
        print("mode set to", self.mode)
        os.system('mkdir "'+ folder +'"')
        self.folder = self.out_folder = folder
        self.file_indexs = { }
    def get_dump_file(self, name, typ):
        fn = self.out_folder +"/"+ name +"__"+ typ +"__"+str(self.file_indexs[name])+".pickle"
        return open(fn, 'wb')
    def get_load_file(self, name, typ):
        fn = self.folder +"/"+ name +"__"+ typ +"__"+str(self.file_indexs[name])+".pickle"
        return open(fn, 'rb')

    def convert_python2_recording_to_python3(self, out_folder):
        self.out_folder = out_folder
        os.system('mkdir "'+ out_folder +'"')
        func_names = [ ] 
        for fn in glob.glob(os.path.join(self.folder ,"*.pickle")):
            func_name = fn[len(self.folder)+1:].split("__")[0]
            if not func_name in func_names:
                func_names.append(func_name)
        for func_name in func_names:
            print(func_name)
            self.file_indexs[func_name] = 1
            fn = self.folder +"/"+ func_name +"__args__"+str(self.file_indexs[func_name])
            while os.path.isfile(self.folder +"/"+ func_name +"__ans__"+str(self.file_indexs[func_name])+".pickle"):
               print("   ", self.file_indexs[func_name])
               for typ in ['args_befor', 'kwargs_befor', 'args_after', 'kwargs_after', 'ans']:
                   #data = pickle.load(self.get_load_file(func_name, typ), encoding='latin1')
                   data = pickle.load(self.get_load_file(func_name, typ), encoding='bytes')
                   print()
                   print("      ", typ)
                   print("      ", data)
                   pickle.dump(data, self.get_dump_file(func_name, typ))  #, encoding='bytes')
               self.file_indexs[func_name] +=1 
        print("Done")

    def is_compare_failed(self, name, typ, actual):
        expected = pickle.load(self.get_load_file(name, typ))
        diff = DeepDiff(expected, actual)
        if len(diff.keys())!=0:
            print("Compare failed for",name, typ)
            print("   Expected is:", expected)
            print("   Actual is:", actual)
            print("   Diff is:", diff)
            print()
            return True
        return False
    def verify(self, func):
        @functools.wraps(func)
        def wrapper_verify(*args, **kwargs):
            name = func.__name__
            if name not in self.file_indexs.keys():
                self.file_indexs[name] = 0
            self.file_indexs[name] +=1 
            if self.mode=="RECORD":
                pickle.dump(args, self.get_dump_file(name, "args_befor"))
                pickle.dump(kwargs, self.get_dump_file(name, "kwargs_befor"))
            elif self.mode=="PLAY_BACK": :
                args = pickle.load(self.get_load_file(name, "args_befor"))
                kwargs = pickle.load(self.get_load_file(name, "kwargs_befor"))
            else:     # VERIFY
                self.is_compare_failed(name, "args_befor", args)
                self.is_compare_failed(name, "kwargs_befor", kwargs)
            ans = func(*args, **kwargs)
            if self.mode=="RECORD":
                pickle.dump(args, self.get_dump_file(name, "args_after"))
                pickle.dump(kwargs, self.get_dump_file(name, "kwargs_after"))
                pickle.dump(ans, self.get_dump_file(name, "ans"))
            else:      # VERIFY or PLAY_BACK
                #if self.is_compare_failed(name, "args_after", args): exit()
                #if self.is_compare_failed(name, "kwargs_after", kwargs): exit()
                #if self.is_compare_failed(name, "ans", ans): exit()
                self.is_compare_failed(name, "args_after", args)
                self.is_compare_failed(name, "kwargs_after", kwargs)
                self.is_compare_failed(name, "ans", ans)
            return ans
        return wrapper_verify

if __name__=="__main__":
    v = Verify("VERIFY", "recording")
    v.convert_python2_recording_to_python3("recording_p3")
