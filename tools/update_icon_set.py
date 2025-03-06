import subprocess, sys, os, glob, re, shutil


def retrieve_unicode_references(webfont_path: str) -> dict:
    unicode_dict : dict = {}
    css_content = open(os.path.join(webfont_path, "tabler-icons.css"),"rt").read()

    matches = re.findall(pattern=r"\.(?:ti-)(.*?)(?::before.*?\"\\)(.*?)(?=\".*?})", flags=re.RegexFlag.S, string=css_content)

    for i,(tag,unicode) in enumerate(matches):
        unicode_dict[tag] = unicode
        print("Icon Progress [{:5} / {:5}]".format(i+1,len(matches)), end='\r')
    print("")
    return unicode_dict


print("Deleting temporary folder")
shutil.rmtree('./tmp',ignore_errors=True)
    

# ---------------------------------------------------------------------------- #
#                          Tabler.io Icons Downloader                          #
# ---------------------------------------------------------------------------- #

# retrieve the latest version
response = subprocess.run(["gh","release","list","--repo","tabler/tabler-icons","-L","1"], check=True, stdout=subprocess.PIPE).stdout.decode().split("\t")
tabler_icons_version = response[2]

print("Version '" + tabler_icons_version + "' retrieved")
print("Downloading release with version '" + tabler_icons_version + "'")

# download said version into a 'tmp' folder
subprocess.run(["gh","release","download","--repo","tabler/tabler-icons","--dir","./tmp",tabler_icons_version])

# ---------------------------------------------------------------------------- #
#                                   Unzipping                                  #
# ---------------------------------------------------------------------------- #
import zipfile

os.chdir("./tmp") # for safety's sake, enter the tmp folder

path = glob.glob("*")[0]
print("Unzipping '" + path + "'")

with zipfile.ZipFile(path + "","r") as zip_ref:
    zip_ref.extractall("./unzipped")

# ---------------------------------------------------------------------------- #
#                         Extracting Unicode References                        #
# ---------------------------------------------------------------------------- #
unicodes = retrieve_unicode_references("./unzipped/webfont/")
os.chdir("..") # go back to script folder

# ------------------------------ Write into file ----------------------------- #
output = open("../_tableau-icons-ref.typ", "wt")

# first write the tabler icons version
tabler_icons_version = tabler_icons_version.replace("v","")

output.write(f"#let tabler-icons-version = \"{tabler_icons_version}\"\n\n")

output.write("#let tabler-icons-unicode = (\n")
for (key, value) in unicodes.items():
    output.write(f"  \"{key}\": \"\\u{{{value}}}\",\n" )
output.write(")")
output.close()

# ---------------------------------------------------------------------------- #
#                         Copy new font somewhere safe                         #
# ---------------------------------------------------------------------------- #
shutil.copy("./tmp/unzipped/webfont/fonts/tabler-icons.ttf","../tabler-icons.ttf")
shutil.copy("./tmp/unzipped/webfont/fonts/tabler-icons.ttf","../fonts/tabler-icons.ttf") # this one is important for compiling the documentation!
shutil.copy("./tmp/unzipped/webfont/fonts/tabler-icons-200.ttf","../tabler-icons-200.ttf")
shutil.copy("./tmp/unzipped/webfont/fonts/tabler-icons-300.ttf","../tabler-icons-300.ttf")

# ---------------------------------------------------------------------------- #
#                                For Doc Header                                #
# ---------------------------------------------------------------------------- #
import random
thumbnail_list = [list(unicodes)[i] for i in (random.sample(range(len(unicodes)), 300))]
thumbnail_file = open("../docs/thumbnail_list.typ", "wt")
thumbnail_file.write("#let thumbnail_list = (\n")
for value in thumbnail_list:
    thumbnail_file.write(f"  \"{value}\",\n" )
thumbnail_file.write(")")
thumbnail_file.close()

# ---------------------------------------------------------------------------- #
#                               Update TOML file                               #
# ---------------------------------------------------------------------------- #
import toml, semver

config = toml.load('../typst.toml')
old_version = semver.Version.parse(config['package']['version'])
tabler_version = semver.Version.parse(tabler_icons_version)

if (str(old_version.minor) == f"{tabler_version.major}{tabler_version.minor}"):
    config['package']['version'] = f"{(old_version.bump_patch())}"
else:
    config['package']['version'] = f"{old_version.major}.{tabler_version.major}{tabler_version.minor}.0"

config['package']['description'] = f"Tabler.io Icons v{tabler_icons_version} for Typst"

f = open("../typst.toml",'w')
toml.dump(config,f)
f.close()

# ---------------------------------------------------------------------------- #
#                             Update Changelog File                            #
# ---------------------------------------------------------------------------- #
file_changelog = open("../docs/changelog.typ", "r")
current_changelog = file_changelog.read()
file_changelog.close()

new_log = f"""== `v{config['package']['version']}`

- updated Tabler Icons version v{tabler_icons_version}
"""

with open("../docs/changelog.typ", "w") as file_changelog:
    file_changelog.write(f"""{new_log}

    {current_changelog}
    """)


input("> Now's your chance to edit the new documents, before they get copied.\n> Once you're done, click enter in this terminal to continue!")

# ---------------------------------------------------------------------------- #
#                 Render the documentation with new information                #
# ---------------------------------------------------------------------------- #
print("compiling documentation")
subprocess.run(["typst","compile","../docs/tableau-icons-doc.typ","--font-path","../fonts","--root",".."])
print("compiling banner")
subprocess.run(["typst","compile","../docs/banner.typ","--format","png","--font-path","../fonts","--root",".."])
# ---------------------------------------------------------------------------- #
#                         Copy project into new folder                         #
# ---------------------------------------------------------------------------- #
print(f"Copying files into '{config['package']['version']}', which can be moved to the typst update folder")
os.makedirs(f"../{config['package']['version']}/docs/",exist_ok=True)
os.chdir(f"../{config['package']['version']}/")

files = [
    ("../docs/banner.png",              "./docs/banner.png"),
    ("../docs/changelog.typ",           "./docs/changelog.typ"),
    ("../docs/tableau-icons-doc.typ",   "./docs/tableau-icons-doc.typ"),
    ("../docs/tableau-icons-doc.pdf",   "./docs/tableau-icons-doc.pdf"),
    ("../docs/thumbnail_list.typ",      "./docs/thumbnail_list.typ"),
    ("../_tableau-icons-ref.typ",       "./_tableau-icons-ref.typ"),
    ("../LICENSE",                      "./LICENSE"),
    ("../README.md",                    "./README.md"),
    ("../tableau-icons.typ",            "./tableau-icons.typ"),
    ("../lib.typ",                      "./lib.typ"),
    ("../.gitignore",                   "./.gitignore"),
    ("../typst.toml",                   "./typst.toml"),
]

for (src, dst) in files:
    shutil.copy(src,dst)


# ------------------------- Rename package references ------------------------ #
print(f"Replacing old package imports with new version {config['package']['version']}")

file = open("./tableau-icons.typ","r")
contents = file.read()
file.close()

contents = re.sub(r"#import \"@preview\/tableau-icons:.+?\": \*",
        repl=f"#import \"@preview/tableau-icons:{config['package']['version']}: *",
        string=contents)

file = open("./tableau-icons.typ","w")
file.write(contents)
file.close()

os.chdir("../tools/")
# ---------------------------------------------------------------------------- #
#                                   Clean Up                                   #
# ---------------------------------------------------------------------------- #
print("Deleting temporary folder")
shutil.rmtree('./tmp')

sys.exit(0)