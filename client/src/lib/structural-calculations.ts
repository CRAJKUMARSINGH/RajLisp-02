import { StaircaseInputs, StaircaseResults } from "@/types/structural";

export function calculateStaircase(inputs: StaircaseInputs): StaircaseResults {
  const {
    clearSpan: lc,
    width: wstr,
    wallWidth: thwall,
    liveLoad: ll,
    floorFinishLoad: ff,
    numRisers: nrise,
    riser: rs,
    tread: td,
    concreteGrade: fck,
    steelGrade: fy
  } = inputs;

  // Basic calculations
  const numTreads = nrise - 1;
  const widthOfGoing = numTreads * td;
  const inclination = Math.sqrt(rs * rs + td * td);

  // Waist slab thickness (assume l/20)
  const thkwsb1 = lc / 20;
  const thkwsb2 = Math.ceil((thkwsb1 + 10) / 10) * 10;
  const thkwsb = thkwsb2;
  
  const clcover = 20;
  const mbar = 12;
  const mbar1 = mbar / 2;
  const edepth = thkwsb - clcover - mbar1;

  // Load calculations
  // 1) Loads on going
  const swstsb = (25 * thkwsb * (inclination / td)) / 1000; // self weight of waist slab
  const swstps = (25 * (rs / 2)) / 1000; // self weight of steps
  const tloadg = swstsb + swstps + ll + ff;
  const ftloadg = tloadg * 1.5;

  // 2) Loads on landing
  const sfsb = (25 * thkwsb) / 1000;
  const tloadl = sfsb + ll + ff;
  const ftloadl = tloadl * 1.5;

  // Bending moment calculation
  const golth = (widthOfGoing + td + (thwall / 2)) / 1000;
  const lanth = (lc / 1000) - golth;
  const raa = (ftloadg * golth) * (golth / 2 + lanth);
  const raaa = ftloadl * (lanth * (lanth / 2));
  const ra = ((raa + raaa) / lc) * 1000;
  const xmax = ra / ftloadg;
  const mmax = ra * xmax - ftloadg * (xmax * xmax) / 2;

  // Main reinforcement
  const breadth = 1000;
  const rrrr = mmax * Math.pow(10, 6);
  const rrr = rrrr / (breadth * edepth * edepth);
  const astm1 = Math.sqrt(1 - (4.6 * rrr) / fck);
  const astm2 = 1 - astm1;
  const astm3 = (edepth * 1000 * 0.5 * fck) / fy;
  const attm = astm2 * astm3;

  // Spacing of main bar
  const bspace1 = (113 * 1000) / attm;
  const bspace2 = Math.floor(bspace1 / 10) * 10;
  const bspace = bspace2;
  const attmp = (113 * 1000) / bspace;

  // Distribution reinforcement
  const astdreq = thkwsb * 0.0012 * 1000;
  const bspaced1 = (50.3 * 1000) / astdreq;
  const bspaced2 = Math.floor(bspaced1 / 10) * 10;
  const bspaced = bspaced2;

  // Check for shear
  const vu = ra - ftloadg * (inclination / 1000);
  const tv = vu / (1 * inclination);
  const pt = (100 * attm) / (1000 * edepth);

  // Simplified shear check (basic implementation)
  let tc = 0.28; // Conservative value for basic check
  if (pt <= 0.15) tc = 0.28;
  else if (pt <= 0.25) tc = 0.36;
  else if (pt <= 0.50) tc = 0.48;
  else if (pt <= 0.75) tc = 0.56;
  else if (pt <= 1.00) tc = 0.62;
  else tc = 0.72;

  const shearSafe = tv < tc;

  // Check for deflection
  const fs = 0.58 * fy * (attm / attmp);
  
  // Simplified modification factor calculation
  let mfactor = 1.0;
  if (fs >= 120 && fs < 145) mfactor = 1.6;
  else if (fs >= 145 && fs < 190) mfactor = 1.4;
  else if (fs >= 190 && fs < 240) mfactor = 1.2;
  else if (fs >= 240 && fs < 290) mfactor = 1.0;
  else mfactor = 0.85;

  const wdepth1 = lc / (mfactor * 20);
  const wdepth = Math.ceil((wdepth1 + 10) / 10) * 10;
  const deflectionSafe = thkwsb >= wdepth1;

  return {
    waistSlabWeight: Math.round(swstsb * 100) / 100,
    stepsWeight: Math.round(swstps * 100) / 100,
    totalLoadGoing: Math.round(tloadg * 100) / 100,
    totalLoadLanding: Math.round(tloadl * 100) / 100,
    factoredLoadGoing: Math.round(ftloadg * 100) / 100,
    factoredLoadLanding: Math.round(ftloadl * 100) / 100,
    
    numTreads,
    widthOfGoing,
    inclination: Math.round(inclination * 100) / 100,
    waistThickness: thkwsb,
    effectiveDepth: edepth,
    
    reaction: Math.round(ra * 100) / 100,
    maxMomentDistance: Math.round(xmax * 100) / 100,
    maxMoment: Math.round(mmax * 100) / 100,
    
    mainSteelArea: Math.round(attm),
    barSpacing: Math.round(bspace1),
    providedSpacing: bspace,
    providedSteelArea: Math.round(attmp),
    
    distributionSteelArea: Math.round(astdreq),
    distributionSpacing: bspaced,
    
    shearStress: Math.round(tv * 100) / 100,
    allowableShear: Math.round(tc * 100) / 100,
    shearSafe,
    deflectionSafe,
    modificationFactor: Math.round(mfactor * 100) / 100,
    recommendedDepth: wdepth
  };
}
