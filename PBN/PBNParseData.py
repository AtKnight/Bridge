from Game import Game

class PbnParseData:
    def __init__(self):
        self.game = Game()
        self.max = 17
        self.filled = False  # No data has been read.

        self.EMPTY = ""
        self.data = []      # Content of a tag
        for i in range(self.max):
            self.data.append(self.EMPTY)
            
        self.nameIndex = {}
        self.unCheckedTags = []

        # See https://www.tistis.nl/pbn/
        # version 2.1

        # Import format: The order of tags is unimportant; the use of (superfluous)
        # tabs and space characters does not matter, etc.
        # In import format, a tag pair that already occurred, is ignored.
        #
        # Export format: The export format is rather strict and is used to describe
        # data that is usually prepared under program control.
        # Tag pairs may only occur once.

        # The escape character "%" in the first column means that the rest of the line
        # can be ignored.
        # A percent sign appearing in any other place other than the first position
        # in a line does not trigger the escape mechanism.

        # % is proposed used for:
        #   (1) It indicates the version of the PBN standard used by a computer program. The syntax is: 
        # % PBN <major version #>.<minor version #>
        #   (2) It indicates that a PBN file has export format. The syntax is: 
        # % EXPORT

        # ; Comment to the end of line.
        # { Lines of comments }
        # Within comments:
        #       \S = Spades, \H = Hearts, \D = Diamonds, \C = Clubs.
        # Comments cannot appear inside any token, nor inside a tag pair.
        # Brace comments do not nest.
        # Special characters lose their meaning inside a comment.

        # A PBN file may contain several games.
        # They are seperated by empty lines of lines with white spaces.

        # A PBN game consists of several sections: 
        # (1) the identification section, 
        # (2) the auction section, 
        # (3) the play section, and 
        # (4) supplemental sections.
        #     This section will be ignored

        # Token:
        # Tokens may be separated from adjacent tokens by white space
        # characters. (White space characters include space, newline,
        # and tab characters.)
        # A white space character can never be part of a token.
        # As a consequence, a token does not cross a text line boundary,
        # and its length is limited to a maximum of 255 characters.

        # Identification Section
        # ======================

        # the name of the tournament or match
        self.nameIndex["Event"] = 0
        self.unCheckedTags.append("Event")

        # the location of the event
        self.nameIndex["Site"] = 1
        self.unCheckedTags.append("Site")

        # the starting date of the game (String)
        # standard ten character format: "YYYY.MM.DD"
        self.nameIndex["Date"] = 2

        # the board number 
        # positive integer (String)
        self.nameIndex["Board"] = 3

        # the west player
        # Dalen van, Gerrit
        # Groot, K.J.R.  
        self.nameIndex["West"] = 4
        self.unCheckedTags.append("West")

        # the north player
        self.nameIndex["North"] = 5
        self.unCheckedTags.append("North")

        # the east player
        self.nameIndex["East"] = 6
        self.unCheckedTags.append("East")

        # the south player
        self.nameIndex["South"] = 7
        self.unCheckedTags.append("South")

        # the dealer
        # W N E S (quoted String)
        self.nameIndex["Dealer"] = 8

        # the situation of vulnerability
        # "None" , "Love" or "-" means no vulnerability
        # "NS"                   means North-South vulnerable
        # "EW"
        # "All" or "Both"	 means both sides vulnerable
        # In export format the tag values "None" and "All" are applied.
        #    =============                ======     =====
        self.nameIndex["Vulnerable"] = 9

        # the dealt cards
        # Example: "N:.63.AKQ987.A9732 A8654.KQ5.T.QJT6 J973.J98742.3.K4 KQT2.AT.J6542.85"
        # means North N: (otherwise: E: S: W:)
        # Notice the space at the end of a hand, except for the last hand.
        # The ranks are defined as (in descending order): A , K , Q , J , T , 9 , 8 , 7 , 6 , 5 , 4 , 3 , 2.
        #            S
        #            H 6 3
        #            D A K Q 9 8 7
        #            C A 9 7 3 2
        # S K Q 10 2                      S A 8 6 5 4
        # H A 10                          H K Q 5
        # J 6 5 4 2                       D 10
        # C 8 5                           C Q J 10 6
        #            S J 9 7 3
        #            H J 9 8 7 4 2
        #            D 3
        #
        # Not all 4 hands need to be given.
        # A hand whose cards are not given, is indicated by "-".
        # For example, only the east/west hands are given: 
        # Deal "W:KQT2.AT.J6542.85 - A8654.KQ5.T.QJT6 -"]
        #
        # In import format, the ranks of a suit can be given in any order; the value of <first> is free.
        # In export format, the ranks must be given in descending order; <first>
        self.nameIndex["Deal"] = 10

        # the scoring method
        # Examples of basic scoring systems are: 
        # MP	        MatchPoint scoring 
        # MatchPoints	identical to 'MP' 
        # IMP	        IMP scoring (since 1962) 
        # Cavendish	Cavendish scoring 
        # Chicago	Chicago scoring 
        # Rubber	Rubber scoring 
        # BAM	        Board-A-Match 
        # Instant	apply InstantScoreTable
        # and so on
        self.nameIndex["Scoring"] = 11
        self.unCheckedTags.append("Scoring")

        # the declarer of the contract
        # "W" (West), "N" (North), "E" (East), or "S" (South). 
        self.nameIndex["Declarer"] = 12
        
        # the contract
        # Example: 5HX means 5 hearts doubled
        # "<k><denomination><risk>" 
        # with 
        # <k>	the number of odd tricks, <k> = 1 … 7 
        # <denomination> the denomination of the contract,
        #                being S (spades), H (Hearts), D (Diamonds), C (Clubs), or NT (NoTrump) 
        # <risk>	 the risk of the contract, being void (undoubled), X (doubled), or XX (redoubled)
        self.nameIndex["Contract"] = 13

        # the result of the game
        # "<result>"	number of tricks won by declarer (0 ... 13)
        # "EW <result>"	number of tricks won by EW 
        # "NS <result>"	number of tricks won by NS 
        # "EW <result> NS <result>"	number of tricks won by EW resp. by NS 
        # "NS <result> EW <result>"	number of tricks won by NS resp. by EW
        # A caret character ("^") preceding one of the above tag values indicates that the <result> differs from the actual number of won tricks.
        # When all 4 players pass, then the tag value is an empty string.
        #
        # The Result tag normally gives the final result after the play has ended.
        # This is the case when all 52 cards have been played, or when the Play section (see below) ends with '*'. 
        # The Result tag can also be used to give a partial result.
        # When the play has not ended, then the Result tag indicates the number of won tricks
        # for the completed, played tricks in the play section.
        #
        # Usage of '+' in the play section (see below) would make it explicitly clear
        # that the Result tag is based on a partial result.
        #
        # In export format the tag value contains the number of tricks won by declarer.
        self.nameIndex["Result"] = 14

        # Auction Section
        # ===============
        # This starts with e.g. [Auction "N"]
        # The direction of the player making the first call is given as tag
        # value in the Auction tag pair: "W", "N", "E" , or "S"
        # In export format this player is always the dealer.
        # In import format the player in the Auction tag value need not be
        # the dealer.
        # In that case, each player before the dealer has a hyphen ("-")
        # in the first auction line.
        # The auction section ends with all passes, or with "*".

        # A call is represented by a call token. The possibilities of a call token are:
        # AP	all players pass
        # Pass	the player passes
        # X	the player doubles
        # XX	the player redoubles
        # <k><denomination>	the player bids a contract,
        #       where <k> and <denomination> are defined as in the Contract tag
        # -     it is not yet player's turn to make a call

        # Example:
        # [Auction "N"]
        # 1D      1S   3H =1= 4S
        # 4NT =2= X    Pass   Pass
        # 5C      X    5H     X
        # 1Pass    Pass Pass
        # [Note "1:non-forcing 6-9 points, 6-card"]
        # [Note "2:two colors: clubs and diamonds"]

        # Annotations such as !, !!, ? are ignored.

        # A note token are ignored.
        # A note token is a sequence of one or more digit characters ("0-9")
        # preceded as well as succeeded by the equal sign ("=").
        # This token terminates just after the succeeding equal sign.

        # A Numeric Annotation Glyph ("NAG") is a token,
        # are ignored.
        # A NAG is composed of a dollar sign character ("$") immediately
        # followed by one or more digit characters.
        # It is terminated just prior to the first non-digit character
        # following the digit sequence.
        self.data[15] = ()  # lines of auctions
        self.nameIndex["Auction"] = 15


        # Play Section
        # ============
        # This start with e.g. [Play, "N"]
        # The direction of the player playing the first card is given
        # as tag value in the Play tag pair: "W".
        # In export format this player is always the opening leader,
        # being declarer's left hand opponent.
        # In import format the player in the Play tag value need not be
        # the opening leader.
        # In that case, each player before the opening leader has a
        # hyphen ("-") in the first play line.
        # The play section ends after 13 tricks, or with "*".
        # + in stead of + has as special meaning and will be ignored.

        # Examples:
        # [Play "W]
        # H2 H3 H4 HA
        # +  -  -  CQ

        # [Play "W"]
        # SK =1= H3 S4 S3
        # C5 C2 C6 CK
        # S2 H6 S5 S7
        # C8 CA CT C4
        # D2 DA DT D3
        # D4 DK H5 H7
        # -  -  -  H2
        # *
        # [Note "1:highest of series"]

        # Annotation and Notes like the Auction Section are ignored.
        self.data[16] = ()  # lines of tricks
        self.nameIndex["Play"] = 16

        # Supplemental tags are ignored by this software.

    def getUnCheckedTags(self):
        return tuple(self.unCheckedTags)

    def setTag(self, tag, value):
        index = self.nameIndex[tag]
        
        if self.data[index] == self.EMPTY :
            self.data[index] = value
            print("gezet ", tag, value)
    




