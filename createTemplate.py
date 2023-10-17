import plistlib, os, shutil

class TemplateCreator:
    def __init__(self, template_base_dir: str, project_dir: str, template_name: str, justModifyPlist: bool = False, bundleIdentifier: str = ""):
        self.template_base_dir = template_base_dir
        self.project_dir = project_dir
        self.template_name = template_name
        self.dir_path = f"{template_base_dir}/{template_name}.xctemplate"
        self.plist_path = f"{self.dir_path}/TemplateInfo.plist"
        self.nodes = []
        self.definitions = {}
        self.bundleIdentifier = bundleIdentifier

        if(justModifyPlist):
            self.modifyPlist()
        else:
            self.createTemplate()

    def addDirToPlist(self, directory: str, parentDir:str = None):
        for file in os.listdir(directory):
            group = '' if parentDir is None else f'{parentDir}/'
            name = f"{group}{file}"

            if file == ".DS_Store" or file.endswith("entitlements"):
                try:
                    os.remove(f"{self.dir_path}/{file}")
                except:
                    pass
                continue

            if file == "Main.storyboard" and parentDir == "base.lproj":
                self.nodes.append(file)
                self.definitions[file] = {
                    "Path": f"base.lproj/{file}"
                }
                continue

            if os.path.isdir(f"{self.project_dir}/{file}"):
                self.addDirToPlist(f"{self.project_dir}/{file}", parentDir=name)
                continue

            self.nodes.append(name)
            self.definitions[name] = {
                "Path": name
            }
            if(group != ''):
                self.definitions[name]["Group"] = group[0:len(group)-1]

    def modifyPlist(self):
        self.addDirToPlist(self.dir_path)

        pl = None

        with open(f"{self.dir_path}/TemplateInfo.plist", 'rb') as f:
            pl = plistlib.load(f)

            pl["Nodes"] = self.nodes
            pl["Definitions"] = self.definitions
            
        with open(f"{self.dir_path}/TemplateInfo.plist", 'wb') as f:
            plistlib.dump(pl, f, sort_keys=False)

    def createTemplate(self):
        if os.path.isdir(self.dir_path):
            shutil.rmtree(self.dir_path)

        shutil.copytree(self.project_dir, self.dir_path)
        self.addDirToPlist(self.project_dir)

        with open(f"Base.plist", 'rb+') as f:
            pl = plistlib.load(f)

            pl["Nodes"] = self.nodes
            pl["Definitions"] = self.definitions
            pl["Description"] = f"Template for {self.template_name}"
            pl["Identifier"] = f"{self.bundleIdentifier}.{self.template_name}"

            with open(f"{self.dir_path}/TemplateInfo.plist", 'wb') as pf:
                plistlib.dump(pl, pf, sort_keys=False)



if(__name__ == "__main__"):
    template_dir = input("Enter base directory for all templates: ")
    project_dir = input("Enter directory for project: ")
    template_name = input("Enter name for template: ")

    just_modify_plist = input("Create new template or alter existing one? ('c' for create, 'a' for alter) ") == "a"

    bundleID = ""

    if(not just_modify_plist):
        bundleID = input ("Enter base bundle identifier (excluding this template's name): ")
       

    templateCreator = TemplateCreator(template_dir, project_dir, template_name, just_modify_plist, bundleID)

    print("Done!")





