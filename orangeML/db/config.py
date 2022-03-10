from configparser import ConfigParser

def config (filename = r"C:\Users\Lenovo\Documents\Projet MA1\Orange3-Clockwork\orangeML\db\database.ini", section ="postgresql"):
    
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
         db[param[0]] = param [1]

    else:
        raise Exception ('Section {0} not found in the {1} file'.format(section,filename))

    return db