from subprocess import run
import os

def runCmd(cmd, lin=False):
    print("[CMD]", cmd)
    if(run(cmd, shell=lin).returncode != 0): quit()

def setBuildDir(platform, isDebug):
    global plat
    global isDbg
    global buildDir
    plat = platform
    isDbg = isDebug
    buildDir = "bin/"+plat+"/"
    if isDbg: buildDir += "dbg/"
    else: buildDir += "rls/"
    if not os.path.isdir(buildDir): os.makedirs(buildDir)
def getBuildDir(): return buildDir

def build(main, outName, compiler, intermediateOnly=False, extraSwitches="", defines=[], includes=[]):
    if compiler not in ("clang++", "cl", "clang"):
        print("Unkown compiler:", compiler)
        quit()
    
    if buildDir == None:
        print("Build directory not set")
        quit()
    
    defineStr = " "
    if plat == "lin" and compiler == "cl": compiler = "clang++"
    if compiler == "cl":
        for i in defines: defineStr += "/D " + i + "=true "
        defineStr += "/D WIN=true /D LIN=false "
        if isDbg: defineStr += "/D RLS=false /D DBG=true "
        else: defineStr += "/D RLS=true /D DBG=false /O2 "
        for i in includes: defineStr += "/I " + i + " "
    else:
        for i in defines: defineStr += "-D " + i + "=true "
        if plat == "win": defineStr += "-D WIN=true -D LIN=false "
        else: defineStr += "-D WIN=false -D LIN=true "
        if isDbg: defineStr += "-D RLS=false -D DBG=true -O0 -g -gcodeview "
        else: defineStr += "-D RLS=false -D DBG=false -O3 "
        for i in includes: defineStr += "-I " + i + " "
    fileName = buildDir + outName
    buildCmd = None
    if compiler == "cl":
        buildCmd = compiler + " /nologo" + defineStr + extraSwitches + " "
        if intermediateOnly:
            buildCmd += "-c "
            if isDbg: buildCmd += "/Z7 "
            buildCmd += main + " /Fo:" + fileName + ".obj "
        else:
            if isDbg: buildCmd += "/Zi "
            buildCmd += main + " /Fo:" + fileName + ".obj /Fd:" + fileName + ".pdb /Fe:" + fileName + ".exe"
    else:
        buildCmd = compiler + defineStr + extraSwitches + " "
        buildCmd += main + " -o " + fileName + ".out"

    runCmd(buildCmd, plat=="lin")
