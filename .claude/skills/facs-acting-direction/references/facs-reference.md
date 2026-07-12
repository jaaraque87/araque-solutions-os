# FACS Expression Reference

## Contents

- Concept
- Prompt Formula
- Intensity Guidance
- 50 Expression Recipes
- Prompt Templates
- Practical QA

## Concept

FACS means Facial Action Coding System. It is an anatomical system developed by Paul Ekman and Wallace Friesen to describe visible facial movement through Action Units, or AUs. The original manual was published in 1978 and updated in 2002. The Paul Ekman Group describes FACS as useful in research, animation, computer vision, and facial recognition: https://www.paulekman.com/facial-action-coding-system/

FACS does not directly mean "sad", "afraid", or "angry". It describes muscular movements. Emotional interpretation comes from combinations of AUs plus context, intensity, breath, gaze, posture, dialogue, and systems such as EMFACS that select FACS events with possible emotional meaning.

For AI images, FACS helps replace generic emotion prompts with anatomical and performative instructions. Instead of `make her sad`, write the face, energy, and behavior that produce restrained sadness.

## Prompt Formula

```text
EMOTIONAL STATE:
valence: -1 to +1
arousal: -1 to +1
dominance: -1 to +1

FACS:
AU codes with anatomical names and intensity.

PERFORMANCE:
breath, tension, posture, voice/delivery, gaze, jaw, micro-expressions.

VISUAL RESULT:
the emotion the image must communicate.
```

Example:

```text
Create a realistic cinematic close-up portrait.

EMOTIONAL STATE:
valence: -0.75
arousal: +0.80
dominance: -0.30

FACS:
AU4 brow lowerer intensity 0.70,
AU7 lid tightener intensity 0.60,
AU23 lip tightener intensity 0.55,
AU25 lips part intensity 0.40.

PERFORMANCE:
controlled fear, unstable breath, subtle jaw tension, eyes wet but focused, micro-expressions of anticipation and internal pressure.

VISUAL RESULT:
the face must feel emotionally alive, not exaggerated, not theatrical, with realistic muscle tension and cinematic restraint.
```

## Intensity Guidance

- `0.10-0.25`: trace, barely visible micro-expression.
- `0.25-0.45`: subtle but readable.
- `0.45-0.70`: clear cinematic/UGC expression without cartooning.
- `0.70-0.90`: intense emotion, danger of melodrama.
- `0.90-1.00`: extreme, useful for shock, screams, panic, slapstick, horror.

Use anatomical names with AU codes because many image models understand the words better than the code alone.

## 50 Expression Recipes

1. `AU6 + AU12`  
   Genuine smile, real joy, human warmth. Cheeks rise and mouth corners lift believably.

2. `AU12`  
   Controlled social smile, polite and slightly artificial. Useful for fashion, business portraits, e-commerce.

3. `AU6 + AU12 + AU25`  
   Soft laughter, open happiness without becoming extreme. Slightly parted lips, engaged eyes.

4. `AU6 + AU12 + AU26`  
   Energetic laughter, spontaneous physical joy. High arousal, positive valence.

5. `AU12 + AU14`  
   Ambiguous, ironic, seductive, or restrained smile. Strong for fashion editorials.

6. `AU14 + AU23`  
   Lateral mouth tension, emotional control, restrained smile, silent challenge.

7. `AU1 + AU4 + AU15`  
   Visible sadness, vulnerability, emotional pain. Inner brows lift while mouth corners pull down.

8. `AU1 + AU4 + AU15 + AU17`  
   Held-back crying, internal suffering, intense fragility. Chin activation makes the face feel close to breaking.

9. `AU1 + AU4 + AU15 + AU17 + AU25`  
   Sadness with unstable breath, parted lips, as if about to speak or cry.

10. `AU4 + AU7 + AU23`  
    Hard concentration, controlled anger, internal tension. Good for intense characters.

11. `AU4 + AU5 + AU7 + AU23`  
    Cold anger, hard gaze, aggressive control. High dominance.

12. `AU4 + AU5 + AU7 + AU23 + AU24`  
    Repressed anger, sealed lips, rigid jaw. Energy held back.

13. `AU4 + AU7 + AU10 + AU23`  
    Restrained disgust or severe annoyance. Upper lip tightens while gaze compresses.

14. `AU9 + AU10`  
    Clear disgust, wrinkled nose and raised upper lip.

15. `AU9 + AU10 + AU16`  
    Strong disgust, physical repulsion, visible rejection.

16. `AU1 + AU2 + AU5 + AU25`  
    Controlled surprise, open eyes, raised brows, slightly parted mouth.

17. `AU1 + AU2 + AU5 + AU25 + AU26`  
    Strong surprise, sudden shock, jaw opening.

18. `AU1 + AU2 + AU5 + AU26 + AU27`  
    Extreme shock, wide open mouth, very open eyes. Useful for cinematic or horror scenes.

19. `AU1 + AU2 + AU4 + AU5 + AU20 + AU25`  
    Classic fear, brows raised and pulled together, eyes open, lips stretched.

20. `AU1 + AU2 + AU4 + AU5 + AU20 + AU25 + AU26`  
    Panic, high activation, loss of control.

21. `AU4 + AU7 + AU20 + AU25`  
    Restrained fear, anxiety, silent tension. Less theatrical, more realistic.

22. `AU4 + AU7 + AU23 + AU25`  
    Controlled anxiety, tense but open lips, unstable breath.

23. `AU4 + AU7 + AU10 + AU17 + AU23 + AU25`  
    Restrained psychological terror, pain, negative anticipation. Excellent for dramatic close-ups.

24. `AU5 + AU7 + AU23`  
    Alertness, suspicion, extreme attention. Eyes open but tense.

25. `AU7 + AU23 + AU24`  
    Severe control, compressed lips, hidden emotion.

26. `AU17 + AU23 + AU24`  
    Emotional rigidity, holding back words or tears, chin tension.

27. `AU15 + AU17 + AU24`  
    Repressed pain, closed mouth, sadness not openly expressed.

28. `AU1 + AU15 + AU17 + AU24`  
    Composed vulnerability, elegant melancholy, fashion-editorial sadness.

29. `AU41 + AU43 partial`  
    Tiredness, apathy, low energy. Heavy eyelids or nearly closed eyes.

30. `AU41 + AU15`  
    Visual depression, low energy, fallen facial expression.

31. `AU43`  
    Closed eyes, stillness, surrender, meditation, or internal pain depending on context.

32. `AU45`  
    Blink. Useful for video or captured-frame naturalism.

33. `AU46`  
    Wink, complicity, light seduction, irony.

34. `AU7 + AU12 + AU14`  
    Clever, complicit, slightly mischievous smile.

35. `AU6 + AU12 + AU14`  
    Warm smile with personality, not naive.

36. `AU12 + AU25 + AU26`  
    Open speaking smile, social energy, performer charisma.

37. `AU25 + AU26`  
    Natural open mouth, breath, dialogue, light astonishment.

38. `AU25 + AU26 + AU27`  
    Extreme mouth opening, scream, maximum surprise, or explosive laughter.

39. `AU19 + AU25`  
    Visible tongue, playful gesture, provocation, pop attitude, 90s editorial energy.

40. `AU19 + AU12 + AU25`  
    Playful tongue-out expression, rebellious energy, teenage irony, anti-polished fashion attitude.

41. `AU18`  
    Puckered lips, kiss, pout, glamour expression, or childish expression depending on context.

42. `AU18 + AU22`  
    Rounded mouth, soft surprise, "oh" expression, kiss, or cartoon-like expression if pushed too far.

43. `AU22 + AU25`  
    Rounded and open mouth, astonishment, held breath, or vowel pronunciation.

44. `AU20 + AU25`  
    Fear or tension with lips stretched sideways, like a nervous smile.

45. `AU20 + AU23`  
    Social tension, embarrassment, discomfort. Lips stretched but controlled.

46. `AU14 + AU15`  
    Bitterness, sad smile, emotionally contradictory expression.

47. `AU6 + AU15`  
    Painful smile, "I am trying not to break down", very cinematic.

48. `AU1 + AU6 + AU12 + AU15`  
    Moved joy, smile mixed with sadness, emotional eyes.

49. `AU1 + AU4 + AU6 + AU15 + AU17`  
    Emotional crying, deep emotion, pain and tenderness together.

50. `AU4 + AU5 + AU7 + AU10 + AU23 + AU38`  
    Intense anger with disgust and flared nostrils. Aggressive, physical, highly charged face.

## Prompt Templates

### Realistic Cinematic Close-Up

```text
Create a realistic cinematic close-up portrait of [subject].

EMOTIONAL STATE:
valence: [value]
arousal: [value]
dominance: [value]

FACS:
[AU code] [action name] intensity [0.00-1.00],
[AU code] [action name] intensity [0.00-1.00].

PERFORMANCE:
[breath], [jaw tension], [eye behavior], [posture], [micro-expression], [delivery].

VISUAL RESULT:
The face must communicate [final emotion] with [restraint/intensity], emotionally alive, realistic, not theatrical, no generic AI smile.
```

### Compact Image Prompt

```text
[subject], [shot/lighting/style]. Expression: [emotion label as result], valence [x], arousal [y], dominance [z]; FACS: [AU list with names and intensities]. Performance: [breath/gaze/jaw/posture]. Result: [specific emotional read], believable and restrained.
```

### Video Frame Or Lip-Sync Beat

```text
0-4s: Close-up on [speaker]. They deliver "[line]" with [compact FACS phrase], [breath/gaze/jaw note]. Keep the mouth visible and the expression controlled.
```

## Practical QA

- Does the prompt describe visible muscle movement instead of only naming an emotion?
- Are the AUs compatible with the mouth shape needed for speech?
- Does the body support the face through breath, shoulders, neck, hands, and gaze?
- Is the expression too extreme for the requested genre?
- Does the final image communicate the intended result without looking theatrical?
- Did the prompt avoid vague phrases like `sad face`, `angry face`, `make it emotional`, or `real emotion` without anatomical direction?
