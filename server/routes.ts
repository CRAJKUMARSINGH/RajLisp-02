import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { insertProjectSchema, insertCalculationSchema, insertReportSchema } from "@shared/schema";
import { z } from "zod";

export async function registerRoutes(app: Express): Promise<Server> {
  // Get user profile
  app.get("/api/user/:id", async (req, res) => {
    try {
      const userId = parseInt(req.params.id);
      const user = await storage.getUser(userId);
      if (!user) {
        return res.status(404).json({ message: "User not found" });
      }
      res.json(user);
    } catch (error) {
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Get user stats
  app.get("/api/user/:id/stats", async (req, res) => {
    try {
      const userId = parseInt(req.params.id);
      const stats = await storage.getStatsByUserId(userId);
      res.json(stats);
    } catch (error) {
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Get user projects
  app.get("/api/user/:id/projects", async (req, res) => {
    try {
      const userId = parseInt(req.params.id);
      const projects = await storage.getProjectsByUserId(userId);
      res.json(projects);
    } catch (error) {
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Create new project
  app.post("/api/projects", async (req, res) => {
    try {
      const projectData = insertProjectSchema.parse(req.body);
      const project = await storage.createProject(projectData);
      res.status(201).json(project);
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ message: "Invalid project data", errors: error.errors });
      }
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Update project
  app.patch("/api/projects/:id", async (req, res) => {
    try {
      const projectId = parseInt(req.params.id);
      const updates = req.body;
      const project = await storage.updateProject(projectId, updates);
      if (!project) {
        return res.status(404).json({ message: "Project not found" });
      }
      res.json(project);
    } catch (error) {
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Get project calculations
  app.get("/api/projects/:id/calculations", async (req, res) => {
    try {
      const projectId = parseInt(req.params.id);
      const calculations = await storage.getCalculationsByProjectId(projectId);
      res.json(calculations);
    } catch (error) {
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Create calculation
  app.post("/api/calculations", async (req, res) => {
    try {
      const calculationData = insertCalculationSchema.parse(req.body);
      const calculation = await storage.createCalculation(calculationData);
      res.status(201).json(calculation);
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ message: "Invalid calculation data", errors: error.errors });
      }
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Get user calculations (recent activity)
  app.get("/api/user/:id/calculations", async (req, res) => {
    try {
      const userId = parseInt(req.params.id);
      const calculations = await storage.getCalculationsByUserId(userId);
      // Return recent calculations (last 10)
      const recentCalculations = calculations
        .sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime())
        .slice(0, 10);
      res.json(recentCalculations);
    } catch (error) {
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Create report
  app.post("/api/reports", async (req, res) => {
    try {
      const reportData = insertReportSchema.parse(req.body);
      const report = await storage.createReport(reportData);
      res.status(201).json(report);
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ message: "Invalid report data", errors: error.errors });
      }
      res.status(500).json({ message: "Internal server error" });
    }
  });

  // Get user reports
  app.get("/api/user/:id/reports", async (req, res) => {
    try {
      const userId = parseInt(req.params.id);
      const reports = await storage.getReportsByUserId(userId);
      res.json(reports);
    } catch (error) {
      res.status(500).json({ message: "Internal server error" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
