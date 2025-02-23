import { create } from 'zustand';
import { Workflow, WorkflowNode, WorkflowEdge } from '../types/workflow';

interface WorkflowState {
  workflows: Workflow[];
  currentWorkflow: Workflow | null;
  selectedNode: WorkflowNode | null;
  selectedEdge: WorkflowEdge | null;
  // Actions
  setWorkflows: (workflows: Workflow[]) => void;
  setCurrentWorkflow: (workflow: Workflow | null) => void;
  setSelectedNode: (node: WorkflowNode | null) => void;
  setSelectedEdge: (edge: WorkflowEdge | null) => void;
  updateNode: (nodeId: string, updates: Partial<WorkflowNode>) => void;
  updateEdge: (edgeId: string, updates: Partial<WorkflowEdge>) => void;
  addNode: (node: WorkflowNode) => void;
  addEdge: (edge: WorkflowEdge) => void;
  removeNode: (nodeId: string) => void;
  removeEdge: (edgeId: string) => void;
}

export const useWorkflowStore = create<WorkflowState>((set) => ({
  workflows: [],
  currentWorkflow: null,
  selectedNode: null,
  selectedEdge: null,

  setWorkflows: (workflows) => set({ workflows }),
  
  setCurrentWorkflow: (workflow) => set({ 
    currentWorkflow: workflow,
    selectedNode: null,
    selectedEdge: null
  }),

  setSelectedNode: (node) => set({ 
    selectedNode: node,
    selectedEdge: null
  }),

  setSelectedEdge: (edge) => set({ 
    selectedEdge: edge,
    selectedNode: null
  }),

  updateNode: (nodeId, updates) => set((state) => ({
    currentWorkflow: state.currentWorkflow ? {
      ...state.currentWorkflow,
      nodes: state.currentWorkflow.nodes.map((node) =>
        node.id === nodeId ? { ...node, ...updates } : node
      )
    } : null
  })),

  updateEdge: (edgeId, updates) => set((state) => ({
    currentWorkflow: state.currentWorkflow ? {
      ...state.currentWorkflow,
      edges: state.currentWorkflow.edges.map((edge) =>
        edge.id === edgeId ? { ...edge, ...updates } : edge
      )
    } : null
  })),

  addNode: (node) => set((state) => ({
    currentWorkflow: state.currentWorkflow ? {
      ...state.currentWorkflow,
      nodes: [...state.currentWorkflow.nodes, node]
    } : null
  })),

  addEdge: (edge) => set((state) => ({
    currentWorkflow: state.currentWorkflow ? {
      ...state.currentWorkflow,
      edges: [...state.currentWorkflow.edges, edge]
    } : null
  })),

  removeNode: (nodeId) => set((state) => ({
    currentWorkflow: state.currentWorkflow ? {
      ...state.currentWorkflow,
      nodes: state.currentWorkflow.nodes.filter((node) => node.id !== nodeId),
      edges: state.currentWorkflow.edges.filter(
        (edge) => edge.source !== nodeId && edge.target !== nodeId
      )
    } : null
  })),

  removeEdge: (edgeId) => set((state) => ({
    currentWorkflow: state.currentWorkflow ? {
      ...state.currentWorkflow,
      edges: state.currentWorkflow.edges.filter((edge) => edge.id !== edgeId)
    } : null
  }))
}));
