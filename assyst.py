
class AssystREST:

    def __init__(self, url, username, password, users, tickets,):
        self.url = url
        self.username = username
        self.password = password
        self.users = users
        self.tickets = tickets
    
    def get_tickets(self):
        ticket_data = {'tickets' : {
            '1123434' : {'ASSIGNEDUSER' : 'JARISS', 'CATAGORY' : 'P1 - 4HR'},
            '1123435' : {'ASSIGNEDUSER' : 'IMOORE', 'CATAGORY' : 'P2 - 8HR'},
            '1123436' : {'ASSIGNEDUSER' : 'CFINCK', 'CATAGORY' : 'P2 - 8HR'},
            '1123437' : {'ASSIGNEDUSER' : 'JWOOD', 'CATAGORY' : 'P2 - 8HR'},
            '1123438' : {'ASSIGNEDUSER' : 'IMOORE', 'CATAGORY' : 'P3 - 16HR'},
            '1123439' : {'ASSIGNEDUSER' : 'SABDUL', 'CATAGORY' : 'P3 - 16HR'},
            '1123440' : {'ASSIGNEDUSER' : 'SABDUL', 'CATAGORY' : 'P3 - 16HR'},
            '1123441' : {'ASSIGNEDUSER' : 'JARISS', 'CATAGORY' : 'P3 - 16HR'},
            '1123442' : {'ASSIGNEDUSER' : 'JARISS', 'CATAGORY' : 'P3 - 16HR'},
            '1123443' : {'ASSIGNEDUSER' : 'IMOORE', 'CATAGORY' : 'P3 - 16HR'},
            '1123444' : {'ASSIGNEDUSER' : 'IMOORE', 'CATAGORY' : 'P3 - 16HR'},
            '1123445' : {'ASSIGNEDUSER' : 'JWOOD', 'CATAGORY' : 'P3 - 16HR'},
            '1124448' : {'ASSIGNEDUSER' : 'JARISS', 'CATAGORY' : 'WORK REQUEST'},
            '1125448' : {'ASSIGNEDUSER' : 'IMOORE', 'CATAGORY' : 'SR2 - 4 DAYS'},
            '1126448' : {'ASSIGNEDUSER' : 'CFINCK', 'CATAGORY' : 'SR3 - 10 DAYS'},
            '1127446' : {'ASSIGNEDUSER' : '', 'CATAGORY' : 'P1 - 4HR'},
            '1123445' : {'ASSIGNEDUSER' : '', 'CATAGORY' : 'P2 - 8HR'},
            '1123667' : {'ASSIGNEDUSER' : '', 'CATAGORY' : 'P3 - 16HR'},
            '1143440' : {'ASSIGNEDUSER' : '', 'CATAGORY' : 'WORK REQUEST'},
            '1153444' : {'ASSIGNEDUSER' : '', 'CATAGORY' : 'SR2 - 4 DAYS'},
            '1163428' : {'ASSIGNEDUSER' : '', 'CATAGORY' : 'SR3 - 10 DAYS'},
            }
        }

        return ticket_data

