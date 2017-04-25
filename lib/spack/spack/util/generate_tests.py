import spack
import argparse
import sys
import os
import spack.architecture as sarch
import spack.util.spack_yaml as yaml
import llnl.util.tty as tty

from random import randint
from spack.spec import Spec, ArchSpec


description = "Generates a test files{days, all, xsdk}"


class GenerateTests(object):

    def __init__(self, use_system_compilers,
                 seperate_by_compiler, specific_test_type):
        if use_system_compilers:
            arch = ArchSpec(str(sarch.platform()),
                            'default_os', 'default_target')
            self.compilers = [
                c.spec for c in spack.compilers.compilers_for_arch(arch)]
        else:
            self.compilers = ['gcc@4.4.7', 'gcc@4.7.4',
                              'gcc@4.8.5', 'gcc@4.8', 'gcc@4.9.3', 'gcc@5.4.0']

        self.xsdk = ['xsdk', 'xsdktrilinos', 'trilinos', 'superlu-mt',
                     'superlu-dist', 'petsc', 'superlu', 'hypre', 'alquimia']

        self.cdash = "https://spack.io/cdash/submit.php?project=spack"
        self.seperate_by_compiler = seperate_by_compiler

        methods = {'all-tests': self.generate_all_tests,
                   'xsdk': self.generate_xsdk,
                   'days': self.generate_days}
        if specific_test_type in methods:
            methods[specific_test_type]()
        else:
            raise Exception("Method %s not implemented" % specific_test_type)

    def seperate_compilers(self, complr_list):
        rtn_dict = {}
        for cmpr in complr_list:
            cmpr = str(cmpr)
            cmplr_name = cmpr.split('@')[0]
            cmplr_version = cmpr.split('@')[1]
            if cmplr_name not in rtn_dict.keys():
                rtn_dict[cmplr_name] = {'version:': []}
                rtn_dict[cmplr_name]['version:'].append(cmplr_version)
            else:
                rtn_dict[cmplr_name]['version:'].append(cmplr_version)
        return rtn_dict

    def generate_all_tests(self):
        self.generate_days()
        self.generate_all()
        self.generate_xsdk()

    def generate_packages(self, compiler,  pkg_list):
        pkgs = {}
        rm_list = []
        num_pkgs = len(pkg_list)
        for sub_pkg in pkg_list:
            # Fill in the entries one by one
            pkg_details = spack.repo.get(sub_pkg)
            version_list = []
            for version in pkg_details.versions:
                version_list.append(str(version))
            pkgs[sub_pkg] = {'versions': version_list}
        for rm_pkg in rm_list:
            tmp_pkg_list.remove(rm_pkg)
        num_pkgs = num_pkgs - len(rm_list)
        if self.seperate_by_compiler:
            pkg_cmplrs = [{"packages": pkgs},
                          self.seperate_compilers(self.compilers)]
        else:
            pkg_cmplrs = [{"packages": pkgs},
                          self.seperate_compilers([compiler])]
        return pkg_cmplrs

    def file_output(self, pkgs, compiler):
        file_dict = {}
        file_dict["test-suite"] = {}
        file_dict["test-suite"]["include"] = pkgs
        file_dict[
            "test-suite"]["matrix"] = self.generate_packages(compiler, pkgs)
        file_dict["test-suite"]["cdash"] = [self.cdash]
        return file_dict

    def generate_days(self):
        # days 1-7
        all_pkgs = spack.repo.all_package_names()
        for compiler in self.compilers:
            for day in range(1, 8):
                tmp_pkg_list = list(all_pkgs)
                num_pkgs = len(tmp_pkg_list)
                if self.seperate_by_compiler:
                    path = os.path.join(os.getcwd(), "day" +
                                        str(day) + "_" + str(compiler) + ".yaml")
                else:
                    path = os.path.join(os.getcwd(), "day" +
                                        str(day) + ".yaml")
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
                    print yaml.dump(self.file_output(day_list, compiler),
                                    default_flow_style=False)

    def generate_all(self):
        all_pkgs = list(spack.repo.all_package_names())
        for compiler in self.compilers:
            if self.seperate_by_compiler:
                path = os.path.join(os.getcwd(), "all_" +
                                    str(compiler) + ".yaml")
            else:
                path = os.path.join(os.getcwd(), "all.yaml")
            with open(path, 'w') as f:
                sys.stdout = f
                print yaml.dump(self.file_output(all_pkgs, compiler),
                                default_flow_style=False)

    def generate_xsdk(self):
        xsdk_pkgs = self.xsdk
        for compiler in self.compilers:
            if self.seperate_by_compiler:
                path = os.path.join(os.getcwd(), "xsdk_" +
                                    str(compiler) + ".yaml")
            else:
                path = os.path.join(os.getcwd(), "xsdk.yaml")
            with open(path, 'w') as f:
                sys.stdout = f
                print yaml.dump(self.file_output(xsdk_pkgs, compiler),
                                default_flow_style=False)
