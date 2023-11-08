import functools, os, pickle
from deepdiff import DeepDiff

class Verify():
    def __init__(self, mode, folder):
        if mode not in ["RECORD", "VERIFY"]:
            print("ERROR: Mode paramter should be RECORD or VERIFY - Aborting")
            exit()
        self.mode = mode
        print("mode set to", self.mode)
        os.system("mkdir -p '"+folder+"'")
        self.folder = folder
        self.file_indexs = { }
    def get_dump_file(self, name, typ):
        fn = self.folder +"/"+ name +"__"+ typ +"__"+str(self.file_indexs[name])+".pickle"
        return open(fn, 'wb')
    def get_load_file(self, name, typ):
        fn = self.folder +"/"+ name +"__"+ typ +"__"+str(self.file_indexs[name])+".pickle"
        return open(fn, 'rb')
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
            else:
                #if self.is_compare_failed(name, "args_befor", args): exit()
                #if self.is_compare_failed(name, "kwargs_befor", kwargs): exit()
                self.is_compare_failed(name, "args_befor", args)
                self.is_compare_failed(name, "kwargs_befor", kwargs)
            ans = func(*args, **kwargs)
            if self.mode=="RECORD":
                pickle.dump(args, self.get_dump_file(name, "args_after"))
                pickle.dump(kwargs, self.get_dump_file(name, "kwargs_after"))
                pickle.dump(ans, self.get_dump_file(name, "ans"))
            else:
                #if self.is_compare_failed(name, "args_after", args): exit()
                #if self.is_compare_failed(name, "kwargs_after", kwargs): exit()
                #if self.is_compare_failed(name, "ans", ans): exit()
                self.is_compare_failed(name, "args_after", args)
                self.is_compare_failed(name, "kwargs_after", kwargs)
                self.is_compare_failed(name, "ans", ans)
            return ans
        return wrapper_verify
