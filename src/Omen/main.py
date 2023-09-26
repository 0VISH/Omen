from subprocess import run
import os

def runCmd(cmd, lin=False):
    print("[CMD]", cmd)
    if(run(cmd, shell=lin).returncode != 0): quit()

def build(main, plat, isDbg, outName, compiler, intermediateOnly=False, extraSwitches=""):

    if compiler not in ("clang++", "cl", "clang"):
        print("Unkown compiler:", compiler)
        quit()
    
    buildDir = "bin/"+plat+"/"
    if isDbg: buildDir += "dbg/"
    else: buildDir += "rls/"

    if not os.path.isdir(buildDir): os.makedirs(buildDir)
    
    defineStr = None
    if compiler == "cl":
        if plat == "win": defineStr = " /D WIN=true /D LIN=false "
        else: defineStr = " /D WIN=false /D LIN=true "
        if isDbg: defineStr += "/D RLS=false /D DBG=true "
        else: defineStr += "/D RLS=true /D DBG=false /O2 "
    else:
        if plat == "win": defineStr = " -D WIN=true -D LIN=false "
        else: defineStr = " -D WIN=false -D LIN=true "
        if isDbg: defineStr += "-D RLS=false -D DBG=true -O0 -g -gcodeview "
        else: defineStr += "-D RLS=false -D DBG=false -O3 "

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
        buildCmd += main + " -c -o "+fileName
        if plat == "win": buildCmd += ".obj "
        else: buildCmd += ".o "
        if intermediateOnly == False:
            buildCmd += "-o " + fileName

    runCmd(buildCmd, plat=="lin")
