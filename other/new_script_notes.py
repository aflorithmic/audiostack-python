scriptText = """"
    <<soundSegment::intro>><<sectionName::intro>> Hello some brand name <<media::branding1>>
"""

mediaFiles={"branding1" : "x123095u1"}


scriptTextv1 = """

<<soundSegment::intro>><<sectionName::intro>>
Hello world and welcome to API audio v2.
<<soundEffect::gunshot>>
Lets play a media item
<<media::branding1>>
"""



scriptTextv2 = """

<<section name="1" soundSegment="intro">>
Hello world and welcome to API audio v2.
<<fx name="gunshot>>
Lets play a media item
<<media name="branding1">> 

"""

#OR <<media placeholder="itemA">>