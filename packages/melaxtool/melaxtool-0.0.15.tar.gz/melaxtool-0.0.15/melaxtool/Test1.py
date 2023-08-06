from melaxtool.melaxapi import MelaxClient

if __name__ == '__main__':
    import os

    # copy your key  to set env below
    os.environ[
        'MELAX_TECH_KEY'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIxIiwidXJsIjoiaHR0cDovL2ludGVybmFsLWs4cy1kZWZhdWx0LXRlc3R3ZWJtLTU0MjRkNWQwYTktMTI1MDk5MDgyMi51cy1lYXN0LTIuZWxiLmFtYXpvbmF3cy5jb20ifQ.rqdwll8ZcpkxrfUvwSK1PePQ7mpqAvT_1zZG63gsWeU"

    input1 = """
    123
    """

    input = """
Arousal, Attention, and Cognition, Impaired
   Assessment:
   Assumed care of pt confused (pt
s baseline from over the last two
   nights). As the evening progressed pt became much notably confused.
   Unable to state where he is or the date. Pt hearing people talking and
   hallucinating, pt states
the dog is behind me, I can not get him
   Action:
   HO made aware of the increase confusion, pt continuously being
   reoriented.
   Response:
   Pt continues to be confused.
   Plan:
   Continue to reorient pt to person, place and time.
   Hypotension (not Shock)
   Assessment:
   Assumed care of pt on vasopressin at 2.4units/hr.  Levophed was at
   0.2mcg/kg/min. ABP dependent on position r/t aline mounted on pt arm.
   ABP mean 55-72
   Action:
   Aline changed to pole mount. MABP increased 70-90
s, able to slowly
   titrate levophed to off while maintaining an adequate ABP. Levophed was
   also decreased to 0.18mcg. Pt tolerated this change well.
   Response:
   Eventually MABP decreased to 50-57, and levophed was placed on 0.25mcg
   and vasopressin was restarted at 2.4unit. However, Pt
s MABP had never
   adequately responded. Of note Pt does respond well to fluid boluses.
   Plan:
   Continue to monitor B/P and maintain MAP >55.
   Hepatorenal syndrome
   Assessment:
   Assumed care of Pt running CRRT fluid balance even.  Skin color remains
   Yellow/bronze colored.  Majority of the shift pt very lethargic, He is
   only oriented x [**11-20**] getting worse as the shift continued. WBC
   increasing.
   Action:
   He remains on lactulose qid with large amount of liquid golden stool
   draining into flexiseal. Remains on IV Vanco, Zosyn, and PO Cipro.
   Attempt made to run pt 25cc negative.
   Response:
   Pt hypotensive does not tolerate any fluid removal. Pt was given back
   150cc with no adequate response. CRRT filter changed per protocol. Hct
   down to 24.8 (guiac +).
   Plan:
   Run pt even on CRRT. Pt to get two units of PRBC, the first unit is to
   run as a bolus over 1hr and then next unit to be run over 2hrs. family
   mgting today at 4PM, Please call transplant team, if available they
   will attend.
   Impaired Skin Integrity
   Assessment:
   Dressings changed on buttocks, left lower extremity draining large
   amounts of  serous fluid. Increased amount of blisters noted on left
   lower leg.
   Action:
   Dressings changed, skin barrier ointment placed on intact skin.
   Response:
   Continue to monitor
   Plan:
   Change dressings PRN, monitor for new open area.

"""

    # client = MelaxClient('/Users/lvjian/key.txt')

    client = MelaxClient()
    print(client.url)

    #
    response = client.invoke(input1, "tf-clinical-pipeline-container:v1.0.0")
    print(response)

    # clinical
    # response = client.visualization(input, "tf-clinical-pipeline-container:v1.0.0")
    # response = client.visualization(input, "vte-pipeline")

# print(len(response.getAllSentence()))


# print(len(response.getAllSentence()))
