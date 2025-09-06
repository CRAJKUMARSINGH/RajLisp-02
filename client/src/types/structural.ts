export interface StaircaseInputs {
  clearSpan: number;
  width: number;
  wallWidth: number;
  liveLoad: number;
  floorFinishLoad: number;
  numRisers: number;
  riser: number;
  tread: number;
  concreteGrade: number;
  steelGrade: number;
}

export interface StaircaseResults {
  // Load calculations
  waistSlabWeight: number;
  stepsWeight: number;
  totalLoadGoing: number;
  totalLoadLanding: number;
  factoredLoadGoing: number;
  factoredLoadLanding: number;

  // Geometry
  numTreads: number;
  widthOfGoing: number;
  inclination: number;
  waistThickness: number;
  effectiveDepth: number;

  // Bending moment
  reaction: number;
  maxMomentDistance: number;
  maxMoment: number;

  // Reinforcement
  mainSteelArea: number;
  barSpacing: number;
  providedSpacing: number;
  providedSteelArea: number;

  // Distribution reinforcement
  distributionSteelArea: number;
  distributionSpacing: number;

  // Checks
  shearStress: number;
  allowableShear: number;
  shearSafe: boolean;
  deflectionSafe: boolean;
  modificationFactor: number;
  recommendedDepth: number;
}

export interface DesignModule {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  status: 'active' | 'coming-soon';
  lastUsed?: string;
  standards: string[];
  category?: 'structural' | 'transportation' | 'geotechnical' | 'hydraulic';
}

export interface ProjectStats {
  activeProjects: number;
  calculations: number;
  reports: number;
  timeSaved: string;
}

export interface RecentActivity {
  id: number;
  type: string;
  projectName: string;
  description: string;
  timeAgo: string;
  icon: string;
  color: string;
}
