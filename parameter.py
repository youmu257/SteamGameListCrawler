# encoding=utf-8
class parameter:
    def __init__(self):
        self.pages = 1
        self.maxPages = 1
        self.getMaxPages = True
        self.saveJson = False
        self.saveDB = False
    def __print__(self):
        print('page = '        + str(self.pages))
        print('maxPages = '    + str(self.maxPages))
        print('getMaxPages = ' + str(self.getMaxPages))
        print('saveJson = '    + str(self.saveJson))
        print('saveDB = '      + str(self.saveDB))
    
def parseArgv(argv):
    arg = parameter()
    if len(argv) < 2:
        # not argument
        print('Using default parameter.')
    print(argv)
    i = 1
    argvLen = len(argv)

    while i < argvLen:
        if argv[i].startswith('--'):
            option = argv[i][2:] # get option
            if option == 'help':
                print('Parameter : \n[--page start_page (end_page)]  setting search start page and end page. It will search total page if not input end page.\n' + 
                      '[--json]  save result as a json file named result.json\n' +
                      '[--db]  save result into database.' )
            elif option == 'page':
                # start page
                if i+1 < argvLen and argv[i+1].isdigit():
                    arg.pages = int(argv[i+1])
                else: 
                    print('page value error! no page number or value is not a integer.')
                i += 1
                # max page
                if i+1 < argvLen:
                    if argv[i+1].isdigit():
                        arg.maxPages = int(argv[i+1])
                        arg.getMaxPages = False
                        i += 1
                    # else: only assign start page
            elif option == 'json':
                # save as json
                arg.saveJson = True
            elif option == 'db':
                # save into db
                arg.saveDB = True
            else:
                print(argv[i] + ' is a unknow parameter. Please use --help to get all parameter.')
        else:
            print(argv[i] + ' is a unknow parameter. Please use --help to get all parameter.')
        i += 1
    return arg
