stage1={    '06 12 01 07 { 15 11 01 25 14 05 24 20 }':'text',
            '..-. .-.. .- --. { .-. . -- --- .-. ... . -....- -.-. --- -.. . ..--.. }':'text'
            }
answers1=['FLAG{OKAYNEXT}','FLAG{REMORSE-CODE?}']

stage2={    'Find the hidden <p hidden>FLAG{SO-SOON}</p>flag here':'text',
            'Okay one more...<p hidden>FLAG{SO-OBVIOUS}</p>':['Not','So','Fast'],
            'Last one<p hidden>Not everytime... Look elsewhere</p>':'text'
            }
answers2=['FLAG{SO-SOON}','FLAG{SO-OBVIOUS}','FLAG{GREAT-JOB}']

stage3={    'Can you crack this <a style="text-decoration:none;" href="/static/Vault.java">vault</a> ?':'text',
            'And <a style="text-decoration:none;" href="/static/Vault2.java">this one</a> too..':'text'
            }
answers3=['FLAG{ju5t-s1mpl3-an4gram5}','FLAG{THEY-WONT-KNOW}']

stage4={    'Shadier than it looks..<br><img style="max-width: 250px;" src="/static/shady.svg">':'text',
            'What is this?? <br><img style="max-width: 250px;" src="/static/binary.png">':'text'
            }
answers4=['FLAG{FOUND-IT}','FLAG{ZIP-IT}']

stage5={    'Where are the seo bots?':'text'
            }
answers5=['FLAG{THE-BOTS-ARE-HERE}']

stage6={    '''I have several such 7 Segment Displays(with only 7-Bit Input):<br>
            <img style="max-width: 250px;" src="/static/7segment.jpg"><br>
            And a Hex Password: 8E3BBDE6205BF71DF8087<br>
            Help me find the flag''':'text'
            }
answers6=['FLAG{-HALO-}']

stage7={    '''Spot the Differences:<br>
            <img style="max-width: 250px;" src="/static/spot1.png">
            <img style="max-width: 250px;" src="/static/spot2.png">''':'text'
            }
answers7=['FLAG{NICE_EYE}']

stage8={    'Find the next flag in <a style="text-decoration:none;" href="/static/Run">this executable</a>':'text'
            }
answers8=['FLAG{PLAY-WITH-ENCODING}']

stage9={    'Where\'s the next flag? Send your queries <a style="text-decoration:none;" href="/api">here</a>':'text',
            'This flag can only be accessed using CSABrowser':'text'
            }
answers9=['FLAG{MY-FIRST-QUERY}','FLAG{SECRET-AGENT-QUERY}']
apistage='9'

questionSet=[stage1,stage2,stage3,stage4,stage5,stage6,stage7,stage8,stage9]
answerSet=[answers1,answers2,answers3,answers4,answers5,answers6,answers7,answers8,answers9]
