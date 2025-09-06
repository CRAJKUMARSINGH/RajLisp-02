(defun savevars()
  (setq clth(get_tile "clength"))
  (setq wstr1(get_tile"wstair"))
  (setq thwall1(get_tile"bwid"))
  (setq livel(get_tile "lload"))
  (setq fload(get_tile "ffload"))
  (setq nrise1(get_tile "nriser"))
  (setq rise(get_tile "riser"))
  (setq trd(get_tile "tread"))
  (setq fck1(get_tile "cgrade"))
  (setq fy1(get_tile "sgrade")))
  
(defun c:stair()
  (defun nirmal()   ;Initialation_Code
       (setq _x_ (dimx_tile "staircase"))
       (setq _y_ (dimy_tile "staircase"))
       (start_Image "staircase")
       (slide_image 0 0 _x_ _y_  "staircase.sld")
       (end_image))
  (setq dcl_id(load_dialog "stair.dcl"))
  (if (not (new_dialog "nirmal" dcl_id) ) (exit))
  (action_tile "cancel" "(setq ddiag 1)(done_dialog)")
  (action_tile "accept" "(setq ddiag 2)(savevars)(done_dialog)")
  
  (nirmal)
  (start_dialog)
  (if(= ddiag 1)
    (*cancel*)
    )
  (if(= ddiag 2)
    (progn
      (princ "\n The user pressed Okay!")
    )
  )
  (princ)
 
  (setq lc(atof clth)
	wstr(atof wstr1)
	thwall(atof thwall1)
	ll(atof livel)
	ff(atof fload)
	nrise(atof nrise1)
	rs(atof rise)
	td(atof trd)
	fck(atof fck1)
	fy(atof fy1))

; CALCULATION OF WIDTH OF GOING

(setq ntread(- nrise 1)
      wgoing(* ntread td))
;sqroot of rsq+tsq

(setq incl(expt (+ (expt rs 2) (expt td 2)) 0.5))

;assume waist slab thickness = l/20

(setq thkwsb1(/ lc 20))
(setq thkwsb2(*(fix (/(+ thkwsb1 10)10))10))
(setq thkwsb(float thkwsb2))
(setq clcover 20)
(setq mbar 12)
(setq mbar1 (/ mbar 2))  
  
(setq edepth(- thkwsb clcover mbar1))

; load calculation
; 1) loads on going

(setq swstsb(/(* 25 thkwsb (/ incl td))1000)) ;  self weight of waist slab
(setq swstps(/(* 25 (/ rs 2))1000))          ; self wt of steps
  (setq tloadg(+ swstsb swstps ll ff))
  (setq ftloadg(* tloadg 1.5))

; 2) loads on landing

  (setq sfsb(/(* 25 thkwsb)1000))
  (setq tloadl(+ sfsb ll ff))
  (setq ftloadl(* tloadl 1.5))

;bending moment calculation

  (setq golth(/(+ wgoing td (/ thwall 2))1000))
  (setq lanth(- (/ lc 1000) golth))
  (setq raa(*(* ftloadg golth) (+ (/ golth 2) lanth))
	raaa(* ftloadl (* lanth (/ lanth 2)))
	ra(*(/(+ raa raaa)lc)1000))
  (setq xmax(/ ra ftloadg))
  (setq mmax(-(* ra xmax) (* ftloadg (/(expt xmax 2)2))))

; main reinforcement
  (setq breadth 1000)
  (setq rrrr(* mmax (expt 10 6)))
  (setq rrr(/ rrrr (* breadth (expt edepth 2))))
  (setq astm1(sqrt (- 1 (/(* 4.6 rrr)fck)))
	astm2(- 1 astm1)
	astm3(/(* edepth(* 1000 (* 0.5 fck )))fy)
	attm(* astm2 astm3))
; spacing of main bar

(setq bspace1(/ (* 113 1000) attm)
      bspace2(*(fix(/ bspace1 10))10)
      bspace(float bspace2)
      attmp(/(* 113 1000)bspace))

; distribution reinforcement

(setq astdreq(* thkwsb (* 0.0012 1000)))
(setq bspaced1(/ (* 50.3 1000) astdreq)
      bspaced2(*(fix(/ bspaced1 10))10)
      bspaced(float bspaced2))

; check for shear

  (setq vu(- ra (* ftloadg (/ incl 1000))))


  ;(8) check in shear
  (setq tv(/ vu(* 1 incl))
	pt(/(* 100 attm)(* 1000 edepth)))

  (cond
    ((<= pt 0.15) (setq tval 0.28) (setq tval2a 0.15) (setq tval2 0.36) (setq tval3 0.25))
    ((and (> pt 0.25) (< pt 0.50) (setq tval 0.36) (setq tval2a 0.25) (setq tval2 0.48) (setq tval3 0.50)))
    ((and (> pt 0.50) (< pt 0.75) (setq tval 0.48) (setq tval2a 0.50) (setq tval2 0.56) (setq tval3 0.75)))
    ((and (> pt 0.75) (< pt 1.00) (setq tval 0.56) (setq tval2a 0.75) (setq tval2 0.62) (setq tval3 1.00)))
    ((and(> pt 1.00) (< pt 1.50)  (setq tval 0.62)(setq tval2a 1.25) (setq tval2 0.72) (setq tval3 1.50)))
    ((and (> pt 1.50) (< pt 1.75) (setq tval 0.72) (setq tval2a 1.50) (setq tval2 0.75) (setq tval3 1.75)))
    ((and (> pt 1.75) (< pt 2.00) (setq tval 0.75) (setq tval2a 1.75) (setq tval2 0.79) (setq tval3 2.00)))
    ((and (> pt 2.00) (< pt 2.25) (setq tval 0.79) (setq tval2a 2.00) (setq tval2 0.81) (setq tval3 2.25)))
    ((and (> pt 2.25) (< pt 2.50) (setq tval 0.81) (setq tval2a 2.25) (setq tval2 0.82) (setq tval3 2.50)))
    ((and (> pt 2.50) (< pt 2.75) (setq tval 0.82) (setq tval2a 2.50) (setq tval2 0.82) (setq tval3 2.75)))
    ((and (> pt 2.75) (< pt 3.00) (setq tval 0.82) (setq tval2a 2.75) (setq tval2 0.82) (setq tval3 3.00)))
    ((> pt 3.00) (setq tval 0.82) (setq tval2a 3.00)))
  (setq tc1(- tval2 tval)
	tc2(- tval3 tval2a)
	tc3(- pt tval2a)
	tc4(/ (* tc1 tc3) tc2)
	tc(+ tval tc4))
  (if
    (< tv tc)(setq tt(strcat" 				tv ("(rtos tv)" Mpa) << tc ("(rtos tc)" Mpa)	hence ok")))

  ; check for deflection

  (setq fs(*(* 0.58 fy) (/ attm attmp))
	pt(/(* 100 attmp)(* 1000 edepth)))
  ; modification factor from IS-456

    (cond
    ((and (>= pt 0.2)(< pt 0.3)(setq fs120 0)(setq fs145 0)(setq fs190 0)(setq fs240 1.68)(setq fs290 1.40)(setq fs1120 0)(setq fs1145 0)(setq fs190 1.89)(setq fs1240 1.47)(setq fs1290 1.23)(setq pt1 0.2)(setq pt2 0.3)))
    ((and (>= pt 0.3)(< pt 0.4)(setq fs120 0)(setq fs145 0)(setq fs190 1.89)(setq fs240 1.47)(setq fs290 1.23)(setq fs1120 0)(setq fs1145 0)(setq fs1190 1.68)(setq fs1240 1.34)(setq fs1290 1.13)(setq pt1 0.3)(setq pt2 0.4)))

    ((and (>= pt 0.4)(< pt 0.5)(setq fs120 0)(setq fs145 0)(setq fs190 1.68)(setq fs240 1.34)(setq fs290 1.13)(setq fs1120 0)(setq fs1145 1.95)(setq fs1190 1.53)(setq fs1240 1.23)(setq fs1290 1.04)(setq pt1 0.4)(setq pt2 0.5)))
    ((and (>= pt 0.5)(< pt 0.6)(setq fs120 0)(setq fs145 1.95)(setq fs190 1.53)(setq fs240 1.23)(setq fs290 1.04)(setq fs1120 0)(setq fs1145 1.79)(setq fs1190 1.43)(setq fs1240 1.17)(setq fs1290 0.98)(setq pt1 0.5)(setq pt2 0.6)))
    ((and (>= pt 0.6)(< pt 0.8)(setq fs120 0)(setq fs145 1.79)(setq fs190 1.43)(setq fs240 1.17)(setq fs290 0.98)(setq fs1120 1.78)(setq fs1145 1.57)(setq fs1190 1.29)(setq fs1240 1.06)(setq fs1290 0.90)(setq pt1 0.6)(setq pt2 0.8)))
    ((and (>= pt 0.8)(< pt 1.0)(setq fs120 1.78)(setq fs145 1.57)(setq fs190 1.29)(setq fs240 1.06)(setq fs290 0.90)(setq fs1120 1.60)(setq fs1145 1.42)(setq fs1190 1.20)(setq fs1240 0.99)(setq fs1290 0.85)(setq pt1 0.8)(setq pt2 1.0)))
    ((and (>= pt 1.0)(< pt 1.2)(setq fs120 1.60)(setq fs145 1.42)(setq fs190 1.20)(setq fs240 0.99)(setq fs290 0.85)(setq fs1120 1.50)(setq fs1145 1.33)(setq fs1190 1.12)(setq fs1240 0.95)(setq fs1290 0.81)(setq pt1 1.0)(setq pt2 1.2)))
    ((and (>= pt 1.2)(< pt 1.4)(setq fs120 1.50)(setq fs145 1.33)(setq fs190 1.12)(setq fs240 0.95)(setq fs290 0.81)(setq fs1120 1.34)(setq fs1145 1.21)(setq fs1190 1.03)(setq fs1240 0.88)(setq fs1290 0.75)(setq pt1 1.2)(setq pt2 1.4)))
    ((and (>= pt 1.4)(< pt 1.6)(setq fs120 1.41)(setq fs145 1.26)(setq fs190 1.08)(setq fs240 0.92)(setq fs290 0.78)(setq fs1120 1.34)(setq fs1145 1.21)(setq fs1190 1.03)(setq fs1240 0.88)(setq fs1290 0.75)(setq pt1 1.4)(setq pt2 1.6)))
    
    ((and (>= pt 1.6)(< pt 1.8)(setq fs120 1.34)(setq fs145 1.21)(setq fs190 1.03)(setq fs240 0.88)(setq fs290 0.75)(setq fs1120 1.30)(setq fs1145 1.17)(setq fs1190 0.99)(setq fs1240 0.85)(setq fs1290 0.72)(setq pt1 1.6)(setq pt2 1.8)))
    ((and (>= pt 1.8)(< pt 2.0)(setq fs120 1.30)(setq fs145 1.17)(setq fs190 0.99)(setq fs240 0.85)(setq fs290 0.72)(setq fs1120 1.23)(setq fs1145 1.12)(setq fs1190 0.97)(setq fs1240 0.83)(setq fs1290 0.71)(setq pt1 1.8)(setq pt2 2.0)))
    ((and (>= pt 2.0)(< pt 2.2)(setq fs120 1.23)(setq fs145 1.12)(setq fs190 0.97)(setq fs240 0.83)(setq fs290 0.71)(setq fs1120 1.20)(setq fs1145 1.10)(setq fs1190 0.94)(setq fs1240 0.82)(setq fs1290 0.70)(setq pt1 2.0)(setq pt2 2.2)))
    ((and (>= pt 2.2)(< pt 2.4)(setq fs120 1.20)(setq fs145 1.10)(setq fs190 0.94)(setq fs240 0.82)(setq fs290 0.70)(setq fs1120 1.18)(setq fs1145 1.06)(setq fs1190 0.91)(setq fs1240 0.81)(setq fs1290 0.69)(setq pt1 2.2)(setq pt2 2.4)))
    ((and (>= pt 2.4)(< pt 2.6)(setq fs120 1.18)(setq fs145 1.06)(setq fs190 0.91)(setq fs240 0.81)(setq fs290 0.69)(setq fs1120 1.15)(setq fs1145 1.04)(setq fs1190 0.90)(setq fs1240 0.80)(setq fs1290 0.68)(setq pt1 2.4)(setq pt2 2.6)))
    ((and (>= pt 2.6)(< pt 2.8)(setq fs120 1.15)(setq fs145 1.04)(setq fs190 0.90)(setq fs240 0.80)(setq fs290 0.68)(setq fs1120 1.13)(setq fs1145 1.02)(setq fs1190 0.89)(setq fs1240 0.79)(setq fs1290 0.67)(setq pt1 2.6)(setq pt2 2.8)))
    ((and (>= pt 2.8)(< pt 3.0)(setq fs120 1.13)(setq fs145 1.02)(setq fs190 0.89)(setq fs240 0.79)(setq fs290 0.67)(setq fs1120 1.11)(setq fs1145 1.00)(setq fs1190 0.88)(setq fs1240 0.78)(setq fs1290 0.67)(setq pt1 2.8)(setq pt2 3.0)))
    ((= pt 3.0)(setq fs120 1.11)(setq fs145 1.00)(setq fs190 0.88)(setq fs240 0.78)(setq fs290 0.67)(setq pt1 2.8)(setq pt2 3.0)))

(setq kfs120 120)
(setq kfs145 145)
(setq kfs190 190)
(setq kfs240 240)
(setq kfs290 290)

; calculation for pt interpolation

   ; fs120

(setq kt120(+ fs120(*(/(- fs1120 fs120)(- pt2 pt1))(- pt pt1))))
  
   ; fs145

(setq kt145(+ fs145(*(/(- fs1145 fs145)(- pt2 pt1))(- pt pt1))))
  
   ; fs190

(setq kt190(+ fs190(*(/(- fs1190 fs190)(- pt2 pt1))(- pt pt1))))
  
   ; fs240

(setq kt240(+ fs240(*(/(- fs1240 fs240)(- pt2 pt1))(- pt pt1))))
  
   ; fs290

(setq kt290(+ fs290(*(/(- fs1290 fs290)(- pt2 pt1))(- pt pt1))))

; calculation for fs interpolation

(cond
  ((and(>= fs kfs120)(< fs kfs145)(setq kkt kt120)(setq kkt1 kt145)(setq fs1 120)(setq fs2 145)))
  ((and(>= fs kfs145)(< fs kfs190)(setq kkt kt145)(setq kkt1 kt190)(setq fs1 145)(setq fs2 190)))
  ((and(>= fs kfs190)(< fs kfs240)(setq kkt kt190)(setq kkt1 kt240)(setq fs1 190)(setq fs2 240)))
  ((and(>= fs kfs240)(< fs kfs290)(setq kkt kt240)(setq kkt1 kt290)(setq fs1 240)(setq fs2 290)))
  ((= fs kfs290)(setq kkt290 kt290)))

(setq mfactor(+ kkt(*(/(- kkt1 kkt)(- fs2 fs1))(- fs fs1))))

; check for deflection

  (setq wdepth1(/ lc (* mfactor 20)))
  (setq wdepth(*(fix (/(+ wdepth1 10)10))10))
	
  



  ; design out put

  (setq f(open "C:\Users\admin\Desktop\stairdesign_result.txt" "w"))

  (setq l2(strcat "			*************************************************************************************")
	l3(strcat "			*	       NXPLORER STRUCTURAL DESIGNER & DEVELOPER (09799468411)		    *")
	l4(strcat "			*************************************************************************************")
	l5(strcat"")
	l6(strcat"   Design of staircase (design code IS-456_2000)  "))
  (setq l7(strcat"   ~~~~~~~~~~~~~~~~~~~  ")
	l8(strcat"")
	l9(strcat"           Design output")
	l10(strcat"                 ")
	z1(strcat"			As per IS-875(1987) Live load = "(rtos ll)" KN/sqm")
	z2(strcat"			 Floor finish load = "(rtos ff)" KN/sqm")
	a10(strcat"					Rise = "(itoa (fix rs))" mm")
	a10a(strcat"					No. of riser = "(itoa (fix nrise))"")
	a11(strcat"					Tread = "(itoa (fix td))" mm")
	a11a(strcat"					No. of Tread = "(itoa (fix ntread))"")
	a12(strcat"					fck = "(itoa (fix fck))" N/sqm")
	a13(strcat"					fy = " (itoa (fix fy))" N/sqm")
	a13aa(strcat"					width of Landing = "(rtos wstr)" mm")
	a13a(strcat"					width of Beam or wall = "(itoa (fix thwall)) " mm")
	a14(strcat"					Effective span = "(itoa (fix lc))" mm")
	a15(strcat"					Length of Going = "(itoa (fix wgoing))" mm")
	a16(strcat"					depth of waist slab according to span depth ratio (l/d = 20) = "(rtos thkwsb1)" mm")
	l10a(strcat"					provide thickness of waist slab = "(itoa (fix thkwsb))" mm")
	b10(strcat"		Load calculation")
	b11(strcat"		~~~~~~~~~~~~~~~~")
	b12(strcat"")
	b13(strcat"				(a) Loads on going")
	b14(strcat"")
	b15(strcat"					1) self weight of waist slab = "(rtos swstsb)" Kn/sqm")
	b16(strcat"					2) self weight of steps = "(rtos swstps) " KN/sqm")
	b17(strcat"					3) Floor finish Load = " (rtos ff)" Kn/sqm")
	b18(strcat"					4) Live load = "(rtos ll)" KN/sqm")
	b19(strcat"					Total load = "(rtos tloadg)" KN/sqm")
	b20(strcat"					Factored Load = "(rtos ftloadg)" KN/sqm")
	b20a(strcat"")
	b21(strcat"				(b) Loads on Landing")
	b22(strcat"")
	b23(strcat"					1) self weight of slab = "(rtos sfsb)" KN/sqm")
	b24(strcat"					2) Live load = "(rtos ll)" KN/sqm")
	b25(strcat"					3) Floor Load = "(rtos ff)" KN/sqm")
	b25(strcat"					Total Load = "(rtos tloadl)" KN/sqm")
	b26(strcat"					Factored Load ="(rtos ftloadl)" KN/sqm")
	b26a(strcat"")
	b27(strcat"		Bending Moment Calculation")
	b28(strcat"		~~~~~~~~~~~~~~~~~~~~~~~~~~")
	b29(strcat"")
	b30(strcat"				Reaction at Left support R1 = "(rtos ra)" KN")
	b31(strcat"				distance at maximum B.M. x = "(rtos xmax)" m")
	b32(strcat"				Maximum B.M. = "(rtos mmax)" Kn/m")
	b32a(strcat"")
	l11(strcat"                 main reinforcement")
	l12(strcat"		 ~~~~~~~~~~~~~~~~~~")
	l13(strcat"					area of steel = "(rtos attm)" sqmm")
	l14(strcat"					use 12 mm dia bar's -")
	l15(strcat"					spacing of bar's = "(rtos bspace1)" mm")
	l16(strcat"					provide 12 mm dia bars @ "(itoa (fix bspace))" mm c/c")
	l16a(strcat"")
	l17(strcat"                Distribution Reinforcement")
        l18(strcat"		~~~~~~~~~~~~~~~~~~~~~~~~~~")
	l19(strcat"					area of steel = "(rtos astdreq)" sqmm")
	l20(strcat"					use 8 mm dia bar's -")
	l21(strcat"					spacing of bar's = "(rtos bspaced1)" mm")
	l22(strcat"					provide 8 mm dia bar @ "(itoa (fix bspaced))" mm c/c")
	l23(strcat"")
	l24(strcat"		check for shear")
	l25(strcat"		~~~~~~~~~~~~~~~")
	l26(strcat"")
	l27(strcat"		check for Deflection")
	l28(strcat"		~~~~~~~~~~~~~~~~~~~~")
	l29(strcat"					span depth ratio  l/d = 20  for simply supproted")
	l30(strcat"					fs = "(rtos fs)" N/sqmm")
	l31(strcat"					modification factor = "(rtos mfactor)"")
	l32(strcat"					Depth according to deflection criteria = "(itoa wdepth)" mm")
	l33(strcat"		Hence provide depth of waist slab = "(itoa wdepth)" mm instead of depth = "(itoa (fix thkwsb))" mm"))
  
	
	
  
  (write-line l2 f)(write-line l3 f)(write-line l4 f)(write-line l5 f)(write-line l6 f)(write-line l7 f)(write-line l8 f)
  (write-line l9 f)(write-line l10 f)(write-line z1 f)(write-line z2 f)(write-line a10 f)(write-line a10a f)(write-line a11 f)(write-line a11a f)(write-line a12 f)(write-line a13 f)(write-line a13a f)(write-line a14 f)(write-line a15 f)(write-line a16 f)(write-line l10a f)(write-line b10 f)(write-line b11 f)
  (write-line b12 f)(write-line b13 f)(write-line b14 f)(write-line b15 f)(write-line b16 f)(write-line b17 f)(write-line b18 f)(write-line b19 f)(write-line b20 f)(write-line b20a f)(write-line b21 f)(write-line b22 f)(write-line b23 f)
  (write-line b24 f)(write-line b25 f)(write-line b26 f)(write-line b26a f)(write-line b27 f)(write-line b28 f)(write-line b29 f)(write-line b30 f)(write-line b31 f)(write-line b32 f)(write-line b32a f)
  (write-line l11 f)(write-line l12 f)(write-line l13 f)(write-line l14 f)
  (write-line l15 f)(write-line l16 f)(write-line l16a f)(write-line l17 f)(write-line l18 f)(write-line l19 f)(write-line l20 f)(write-line l21 f)
  (write-line l22 f)(write-line l23 f)(write-line l24 f)(write-line l25 f)(write-line tt f)(write-line l26 f)(write-line l27 f)
  (write-line l28 f)(write-line l29 f)(write-line l30 f)(write-line l31 f)(write-line l32 f)(write-line l33 f)
  (command "notepad" "C:\Users\admin\Desktop\stairdesign_result.txt"))
  
      






  
 
	
	
	
  