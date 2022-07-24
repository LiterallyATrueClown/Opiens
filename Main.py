import sys
import subprocess
from Options import OptionsBuilder
from Parser.Parser import Parser

from Obfuscator.ObfMain import ObfMain


File = "test.lua"


# Since i dont know the package management thing in python (idk if its called like that) i'll just write without it

class Main:
    def __init__(self):
        self.AstTree = {}
    
    @staticmethod
    def ReadFile():
        FileSrc = ""
        with open(File, 'r') as f:
            FileSrc = f.read()
            f.close()
        
        return FileSrc

    @staticmethod
    def GetOptions(LuaVersion, Dif):
        return OptionsBuilder().BuildSettings(LuaVersion, Dif)

    @staticmethod
    def StartOptimizer():
        try:
            CC = subprocess.Popen(["node", "beautify.js"], stdout=subprocess.PIPE)
            CC.communicate()
            CC.wait()
            
            #out, err = p.communicate()
        except:
            print("[E] Optimizer failed!")
            raise OSError

    def GetAst(self, Source):
        self.AstTree = Parser(Source).Parse()
        return self.AstTree


if __name__ == '__main__':
    """
    Main.py is the main file of the program.
    Currently it has Low and Medium presets.
    Only supports Lua 5.1
    """
    from luaparser import ast
    import random

    IntKey = random.randint(10, 15)
    Main.StartOptimizer()
    

    Source = Main.ReadFile()
    Options = Main.GetOptions("5.1", "Low")
    AstTree, IntDecryptor = ObfMain(Source, Options, IntKey).Obfuscate()
    #AstTree = Main().GetAst(Source) # This will be removed later

    LuaSource = IntDecryptor + "\n"
    LuaSource += ast.to_lua_source(AstTree)
    with open("output.lua", 'w') as f:
        f.write(LuaSource)
        f.close()
    print(LuaSource)
