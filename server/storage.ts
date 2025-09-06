import { 
  users, projects, calculations, reports,
  type User, type InsertUser,
  type Project, type InsertProject,
  type Calculation, type InsertCalculation,
  type Report, type InsertReport
} from "@shared/schema";

export interface IStorage {
  // Users
  getUser(id: number): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;

  // Projects
  getProject(id: number): Promise<Project | undefined>;
  getProjectsByUserId(userId: number): Promise<Project[]>;
  createProject(project: InsertProject): Promise<Project>;
  updateProject(id: number, updates: Partial<Project>): Promise<Project | undefined>;
  deleteProject(id: number): Promise<boolean>;

  // Calculations
  getCalculation(id: number): Promise<Calculation | undefined>;
  getCalculationsByProjectId(projectId: number): Promise<Calculation[]>;
  getCalculationsByUserId(userId: number): Promise<Calculation[]>;
  createCalculation(calculation: InsertCalculation): Promise<Calculation>;

  // Reports
  getReport(id: number): Promise<Report | undefined>;
  getReportsByUserId(userId: number): Promise<Report[]>;
  createReport(report: InsertReport): Promise<Report>;

  // Stats
  getStatsByUserId(userId: number): Promise<{
    activeProjects: number;
    calculations: number;
    reports: number;
    timeSaved: string;
  }>;
}

export class MemStorage implements IStorage {
  private users: Map<number, User>;
  private projects: Map<number, Project>;
  private calculations: Map<number, Calculation>;
  private reports: Map<number, Report>;
  private currentUserId: number;
  private currentProjectId: number;
  private currentCalculationId: number;
  private currentReportId: number;

  constructor() {
    this.users = new Map();
    this.projects = new Map();
    this.calculations = new Map();
    this.reports = new Map();
    this.currentUserId = 1;
    this.currentProjectId = 1;
    this.currentCalculationId = 1;
    this.currentReportId = 1;

    // Initialize with sample user
    this.createUser({
      username: "nirmal",
      name: "Nirmal Suthar",
      email: "nirmal@structuralcad.com"
    });
  }

  async getUser(id: number): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(user => user.username === username);
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = this.currentUserId++;
    const user: User = { 
      ...insertUser, 
      id, 
      createdAt: new Date()
    };
    this.users.set(id, user);
    return user;
  }

  async getProject(id: number): Promise<Project | undefined> {
    return this.projects.get(id);
  }

  async getProjectsByUserId(userId: number): Promise<Project[]> {
    return Array.from(this.projects.values()).filter(project => project.userId === userId);
  }

  async createProject(insertProject: InsertProject): Promise<Project> {
    const id = this.currentProjectId++;
    const now = new Date();
    const project: Project = {
      ...insertProject,
      id,
      createdAt: now,
      updatedAt: now,
      results: insertProject.results || null
    };
    this.projects.set(id, project);
    return project;
  }

  async updateProject(id: number, updates: Partial<Project>): Promise<Project | undefined> {
    const project = this.projects.get(id);
    if (!project) return undefined;

    const updatedProject = {
      ...project,
      ...updates,
      updatedAt: new Date()
    };
    this.projects.set(id, updatedProject);
    return updatedProject;
  }

  async deleteProject(id: number): Promise<boolean> {
    return this.projects.delete(id);
  }

  async getCalculation(id: number): Promise<Calculation | undefined> {
    return this.calculations.get(id);
  }

  async getCalculationsByProjectId(projectId: number): Promise<Calculation[]> {
    return Array.from(this.calculations.values()).filter(calc => calc.projectId === projectId);
  }

  async getCalculationsByUserId(userId: number): Promise<Calculation[]> {
    return Array.from(this.calculations.values()).filter(calc => calc.userId === userId);
  }

  async createCalculation(insertCalculation: InsertCalculation): Promise<Calculation> {
    const id = this.currentCalculationId++;
    const calculation: Calculation = {
      ...insertCalculation,
      id,
      createdAt: new Date(),
      isValid: insertCalculation.isValid || 'true'
    };
    this.calculations.set(id, calculation);
    return calculation;
  }

  async getReport(id: number): Promise<Report | undefined> {
    return this.reports.get(id);
  }

  async getReportsByUserId(userId: number): Promise<Report[]> {
    return Array.from(this.reports.values()).filter(report => report.userId === userId);
  }

  async createReport(insertReport: InsertReport): Promise<Report> {
    const id = this.currentReportId++;
    const report: Report = {
      ...insertReport,
      id,
      createdAt: new Date(),
      format: insertReport.format || 'pdf'
    };
    this.reports.set(id, report);
    return report;
  }

  async getStatsByUserId(userId: number): Promise<{
    activeProjects: number;
    calculations: number;
    reports: number;
    timeSaved: string;
  }> {
    const userProjects = await this.getProjectsByUserId(userId);
    const userCalculations = await this.getCalculationsByUserId(userId);
    const userReports = await this.getReportsByUserId(userId);

    return {
      activeProjects: userProjects.filter(p => p.status === 'active').length,
      calculations: userCalculations.length,
      reports: userReports.length,
      timeSaved: `${Math.floor(userCalculations.length * 2.5)}h`
    };
  }
}

export const storage = new MemStorage();
