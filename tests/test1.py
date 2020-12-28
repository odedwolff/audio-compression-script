#from ...script_compress_audio import convertTreeToMp3
import importlib.util
spec = importlib.util.spec_from_file_location("compAud", "../compAud.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)
#foo.MyClass()
#foo.convertTreeToMp3("C:\temp\test_comp_audio\root", "C:\temp\test_1_out", 20) 

foo.convertTreeToMp3("C:/temp/test_comp_audio/root", "C:/temp/test_1_out", 20) 

#convertTreeToMp3("C:\temp\test_comp_audio\root", "C:\temp\test_1_out", 20)