import sys
import re
import Constantes
import General

from datetime import date
from PBNParseData import PbnParseData

class PBN_IO:

    def __init__(self, fileName) :
        self.fileName = fileName
        self.pbn = PbnParseData()
        self.unCheckedTags = self.pbn.getUnCheckedTags()

    def parseFile(self):
        try:
            self.fileDescr = open(self.fileName, "r")
        except:
            General.fatal_error(f'File {self.fileName} could not be opened')

        self.lineNumber = 0
        
        line = self.readline()
        while not self.eof(line):
            self.parseLine(line)
            line = self.readline()
            # self.fileDescr and self.lineNumber may be changed.

        return self.pbn

    def readline(self):
        self.lineNumber += 1
        line = self.fileDescr.readline()
        
        return line.strip()

    def eof(self, line):
        return line == ''

    def parseLine(self, line):
        if len(line) == 0:
            return

        # comment line
        if line[0] in ('%', ';'):
            return
        
        # multi lines with comment
        if line.startswith('{'):
            self.processComment(line)
            return
            
        if line.startswith("["):
            self.processTag(line)
        else:
            print("onbekende inhoud: ", line)
            

    def processComment(self, line):
        while not self.eof(line) and not '}' in line:
           line = self.readline()

        if not line.endswith('}'):
            General.fatal_error(f'Comment in line {self.linenumber} does not ends with' + '}')

    def processTag(self, line):
        spIndex = line.find(' ')
        assert spIndex > -1

        tag = line[1:spIndex]        # remove [
        restLine = line[spIndex:-1]  # remove \n
        restLine = restLine.strip()
        
        restLine = self.removeQuotes(restLine)
        #remove quotes at the begin and end
        
        print(f'tag = -->{tag}<-->restline = -->{restLine}<--')

        if tag in self.unCheckedTags:
            self.pbn.setTag(tag, restLine)

            return

        if tag == "Date":
            if self.date_ok(restLine):
                self.pbn.setTag(tag, restLine)
            else:
                General.fatal_error(f'Date or dateformat(YYYY.MM.DD) is wrong: {restLine}')

            return

        if tag == "Board":
            if self.board_ok(restLine):
                 self.pbn.setTag(tag, restLine)
            else:
                General.fatal_error(f'Board is not an integer: {restLine}')
                
            return

        if tag == "Dealer":
            if self.direction_ok(restLine):
                 self.pbn.setTag(tag, restLine)
            else:
                General.fatal_error(f'Dealer is invalid: {restLine}')

            return

        if tag == "Declarer":
            if self.direction_ok(restLine):
                 self.pbn.setTag(tag, restLine)
            else:
                General.fatal_error('Declarer is invalid: {restLine}')

            return

        if tag == "Vulnerable":
            if self.vulnerable_ok(restLine):
                 self.pbn.setTag(tag, restLine)
            else:
                General.fatal_error(f'Vulnerable is invalid: {restLine}')

            return

        if tag == "Deal":
            if self.deal_ok(restLine):
                self.pbn.setTag(tag, restLine)
            else:
                General.fatal_error(f'Deal is invalid: {restLine}')

            return
            
            
    def date_ok(self, line):
        if re.search('[1-2][0-9]{3}\.[0-1][0-9]\.[0-3][0-9]', line) is None:
            return False

        year = int(line[0:4])
        month = int(line[5:7])
        day = int(line[8:10])
        
        try:
            date(year, month, day)
        except:
            return False

        return True

    def board_ok(self, restLine):
        try:
            waarde = int(restLine)
        except:
            return False

        return waarde > 0

    def suit_ok(self, str):
        return str in Constantes.SHORT_SUITES

    def direction_ok(self, str):
        return str in Constantes.SHORT_DIRECTIONS

    def vulnerable_ok(self, str):
        return str in ("None" , "Love", "-","NS", "EW", "All", "Both")

    def deal_ok(self, str):
        # "N:.63.AKQ987.A9732 A8654.KQ5.T.QJT6 J973.J98742.3.K4 KQT2.AT.J6542.85"
        if not str[0] in Constantes.SHORT_DIRECTIONS or str[1] != ":":
            return False

        for hand in re.split('\s+', str[2:]):
            print(f'Hand-->{hand}<--')
            suitCards = re.split('\.', hand)
            for sc in suitCards:  # cards in (S, H, D, C)
                print(f'suitCards -->{sc}<--')
                if len(sc) > 0:
                    for i in range(0, len(sc)):  # A, K, Q, J, T ... 2
                        m = re.search(sc[i], 'AKQJT98765432')
                        if m is None:
                            print("Ongeldig ", sc[i])
                            return False

            print("")

        return True





    
        

    def removeQuotes(self, line):
        quote = line[0]

        if quote == line[-1] and quote in ('"', "'"):
            return line[1:-1]

        return line

        
        
        
        
        

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        General.fatal_error("PBN-file is not given")

    pbn_reader = PBN_IO(sys.argv[1])
    result = pbn_reader.parseFile()

    print(result.data)


    
