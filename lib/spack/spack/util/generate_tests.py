#import spack.cmd.list as list
import spack
import argparse
import sys
import spack.util.spack_yaml as yaml
from random import randint
import llnl.util.tty as tty
from spack.spec import Spec

description = "Generates a test files{days, all, xsdk}"


class GenerateTests:

    def __init__(self, all_compilers=True, specific_type="all"):
        if all_compilers:
            self.compilers = ['gcc@4.4.7', 'gcc@4.7.4',
                              'gcc@4.8.5', 'gcc@4.8', 'gcc@4.9.3', 'gcc@5.4.0']
        else:
            arch = ArchSpec(str(sarch.platform()),
                            'default_os', 'default_target')
            self.compilers = [
                c.spec for c in spack.compilers.compilers_for_arch(arch)]

        self.xsdk = ['xsdk', 'xsdktrilinos', 'trilinos', 'superlu-mt',
                'superlu-dist', 'petsc', 'superlu', 'hypre', 'alquimia']

        self.cdash = "https://spack.io/cdash" \
            "/submit.php?project=spack"
        self.all_compilers = all_compilers

        generate_days()
        generate_all()
        generate_xsdk()

    def setup_parser(subparser):
        subparser.add_argument(
            'yamlFile', nargs=argparse.REMAINDER,
            help="Compiles a list of tests from a yaml file. Runs Spec and concretize then produces cdash format.")

    def seperate_compilers(self, complr_list):
        rtn_dict = {}
        for cmpr in complr_list:
            cmplr_name = cmpr.split('@')[0]
            cmplr_version = cmpr.split('@')[1]
            if cmplr_name not in rtn_dict.keys():
                rtn_dict[cmplr_name] = {'version:': []}
                rtn_dict[cmplr_name]['version:'].append(cmplr_version)
            else:
                rtn_dict[cmplr_name]['version:'].append(cmplr_version)
        return rtn_dict

    def generate_packages(self, compiler,  pkg_list):
        pkgs = {}
        for sub_pkg in pkg_list:
            # Fill in the entries one by one
            pkg_details = spack.repo.get(pkg)
            version_list = []
            for version in pkg_details.versions:
                version_list.append(str(version))
            pkgs[sub_pkg] = {'versions': version_list}
        for rm_pkg in rm_list:
            tmp_pkg_list.remove(rm_pkg)
        num_pkgs = num_pkgs - len(rm_list)
        if self.all_compilers:
            pkg_cmplrs=[{"packages":pkgs},seperate_compilers(self.compilers)]
        else:
            pkg_cmplrs=[{"packages":pkgs},seperate_compilers(compiler)]
        return pkg_cmplrs

    def generate_days(self):
        #import spack.cmd.list as list
        # days 1-7
        all_pkgs = spack.repo.all_package_names()
        for compiler in self.compilers:
            for day in range(1, 8):
                tmp_pkg_list = list(all_pkgs)
                num_pkgs = len(tmp_pkg_list)
                path = os.path.join(os.getcwd(), "day" +
                                    str(day) + "_" + compiler + ".yaml")
                with open(path, 'w') as f:
                    sys.stdout = f
                    rm_list = []
                    day_list = []
                    for x in range(num_pkgs / 7):
                        item = tmp_pkg_list[randint(0, num_pkgs - 1)]
                        while item in rm_list:
                            item = tmp_pkg_list[randint(0, num_pkgs - 1)]
                        rm_list.append(item)
                        day_list.append(item)
                    file_dict = {}
                    file_dict["test-suite"] = {}
                    file_dict["test-suite"]["include"] = day_list
                    file_dict["test-suite"]["matrix"] = generate_packages(compiler, day_list)
                    file_dict["test-suite"]["cdash"] = [self.cdash]
                    print yaml.dump(file_dict, default_flow_style=False)

    def generate_all():
        #import spack.cmd.list as list
        all_pkgs = list(spack.repo.all_package_names())
        for compiler in self.compilers:
            path = os.path.join(os.getcwd(), "all_" + compiler + ".yaml")
            with open(path, 'w') as f:
                sys.stdout = f
                file_dict = {}
                file_dict["test-suite"] = {}
                file_dict["test-suite"]["include"] = all_pkgs
                file_dict["test-suite"]["matrix"] = generate_packages(compiler, all_pkgs)
                file_dict["test-suite"]["cdash"] = [self.cdash]
                print yaml.dump(file_dict, default_flow_style=False)

    def generate_xsdk():
        #import spack.cmd.list as list
        xsdk_pkgs = self.xsdk
        for compiler in self.compilers:
            path = os.path.join(os.getcwd(), "xsdk_" + compiler + ".yaml")
            with open(path, 'w') as f:
                sys.stdout = f
                file_dict = {}
                file_dict["test-suite"] = {}
                file_dict["test-suite"]["include"] = xsdk_pkgs
                file_dict["test-suite"]["matrix"] = generate_packages(compiler, xsdk_pkgs)
                file_dict["test-suite"]["cdash"] = [self.cdash]
                print yaml.dump(file_dict, default_flow_style=False)
    '''#remove
    list2 = []
    rmlist = []
    allpkgs = set(spack.repo.all_package_names())
    '''  # remove
    '''
    with open('/Users/friedt2/xsdk.yaml', 'w') as f:
        sys.stdout = f
        finaldict = {}
        for pkg in allpkgs:
            # Fill in the entries one by one
            pkgdetails = spack.repo.get(pkg)
            versionList = []
            for x in pkgdetails.versions:
                versionList.append(str(x))

            finaldict[pkg] = "[{\"versions\": "+str(versionList)+"}]"

        #tty.msg(listz)

        #print finaldict
        yamlf= yaml.dump(finaldict,default_flow_style=False)
        num = 0
        print "---"
        print "enable: [ xsdk, trilinos, petsc, superlu, hypre, chombo, alquimia ]"
        print "exclusions: []"
        print ""
        print "packages:"
        for line in yamlf.split('}]\''):
            line = line.strip()
            try:
                b = line.split(' ')[0] 
                c = line.split(' ')[1].split('[{')[1].split('\"')[1]#    [{"versions":
                d = line.split(':')[2].split('}]')[0].replace("\'\'", "")
                print "  - " +str(b)
                print "    - " +str(c)+":"+str(d)
            except:
                continue
        print """
compilers:
  - gcc:
    - versions: [4.9, 4.8, 4.7, 5.0]
  - clang:
    - versions: [3.5, 3.6, 3.7, 3.8]

dashboard: ["https://spack.io/cdash/submit.php?project=spack"]
"""


'''  # remove
# all in one file
    with open('/Users/friedt2/all.yaml', 'w') as f:
        sys.stdout = f
        for x in allpkgs:
            list2.append(str(x))
        finaldict = {}
        for pkg in list2:
            # Fill in the entries one by one
            pkgdetails = spack.repo.get(pkg)
            versionList = []
            tmp = []
            for x in pkgdetails.versions:
                versionList.append(str(x).rstrip('\r\n  \n   '))
            for x in versionList:
                x.rstrip('\r\n  \n   ')
                tmp.append(x)
            finaldict[pkg] = "[{\"versions\": " + ", ".join(tmp) + "}]"

        yamlf = yaml.dump(finaldict, default_flow_style=False)
        f.write("---\n")
        f.write("test-suite:\n")
        f.write("    include: [ " + str(", ".join(allpkgs)) + "]\n")
        f.write("\n")
        f.write("    packages:\n")
        for line in yamlf.split('}]\''):
            line = line.strip()
            try:
                b = line.split(' ')[0]
                # [{"versions":
                c = line.split(' ')[1].split('[{')[1].split('\"')[1]
                d = line.split(':')[2].split('}]')[0].replace("\'\'", "")
                f.write("        " + str(b) + "\n")
                f.write("            " + str(c) + ": [" + str(d) + "]\n")
            except:
                continue
        f.write("\n")
        f.write("    compilers:\n")
        f.write("        gcc:\n")
        f.write("            versions: [4.9, 4.8, 4.7, 5.0]\n")
        f.write("        clang:\n")
        f.write("            versions: [3.5, 3.6, 3.7, 3.8]\n")
        f.write("\n")
        f.write(
            "    dashboard: [\"https://spack.io/cdash/submit.php?project=spack\"]\n")


# days 1-7 output
    for x in allpkgs:
        list2.append(str(x))
    numPkgs = len(list2)
    for cnt in range(1, 8):
        listz = []
        rmlist = []
        import sys
        with open('/Users/friedt2/day' + str(cnt) + '.yaml', 'w') as f:
            sys.stdout = f
            for x in range(numPkgs / 7):
                item = list2[randint(0, numPkgs - 1)]
                while item in rmlist:
                    item = list2[randint(0, numPkgs - 1)]
                rmlist.append(item)
                listz.append(item)

            finaldict = {}
            for pkg in listz:
                # Fill in the entries one by one
                pkgdetails = spack.repo.get(pkg)
                versionList = []
                for x in pkgdetails.versions:
                    versionList.append(str(x))

                finaldict[pkg] = "[{\"versions\": " + str(versionList) + "}]"
            for item in rmlist:
                list2.remove(item)
            numPkgs = numPkgs - len(rmlist)
            # tty.msg(listz)

            # print finaldict
            yamlf = yaml.dump(finaldict, default_flow_style=False)
            num = 0
            f.write("---\n")
            f.write("test-suite:\n")
            f.write("    include: [ " + str(", ".join(listz)) + "]\n")
            f.write("\n")
            f.write("    packages:\n")
            for line in yamlf.split('}]\''):
                line = line.strip()
                try:
                    b = line.split(' ')[0]
                    # [{"versions":
                    c = line.split(' ')[1].split('[{')[1].split('\"')[1]
                    d = line.split(':')[2].split('}]')[0].replace("\'\'", "")
                    f.write("        " + str(b) + "\n")
                    f.write("            " + str(c) + ":" + str(d) + "\n")
                except:
                    continue
            f.write("\n")
            f.write("    compilers:\n")
            f.write("        gcc:\n")
            f.write("            versions: [4.9, 4.8, 4.7, 5.0]\n")
            f.write("        clang:\n")
            f.write("            versions: [3.5, 3.6, 3.7, 3.8]\n")
            f.write("\n")
            f.write(
                "    dashboard: [\"https://spack.io/cdash/submit.php?project=spack\"]\n")

        f.write("---\n")
        f.write("test-suite:\n")
        f.write("    include: [ " + str(", ".join(allpkgs)) + "]\n")
        f.write("\n")
        f.write("    packages:\n")
        for line in yamlf.split('}]\''):
            line = line.strip()
            try:
                b = line.split(' ')[0]
                # [{"versions":
                c = line.split(' ')[1].split('[{')[1].split('\"')[1]
                d = line.split(':')[2].split('}]')[0].replace("\'\'", "")
                f.write("        " + str(b) + "\n")
                f.write("            " + str(c) + ":[" + str(d) + "]\n")
            except:
                continue
        f.write("\n")
        f.write("    compilers:\n")
        f.write("        gcc:\n")
        f.write("            versions: [4.9, 4.8, 4.7, 5.0]\n")
        f.write("        clang:\n")
        f.write("            versions: [3.5, 3.6, 3.7, 3.8]\n")
        f.write("\n")
        f.write(
            "    dashboard: [\"https://spack.io/cdash/submit.php?project=spack\"]\n")
