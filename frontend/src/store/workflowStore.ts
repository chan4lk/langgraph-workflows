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

  updateNode: (nodeId, updates) => set((state) => {
    if (!state.currentWorkflow) return state;

    const updatedNodes = state.currentWorkflow.nodes.map((node) =>
      node.id === nodeId ? { ...node, ...updates } : node
    );

    // Also update the selected node if it's the one being modified
    const updatedSelectedNode = state.selectedNode?.id === nodeId
      ? { ...state.selectedNode, ...updates }
      : state.selectedNode;

    return {
      currentWorkflow: {
        ...state.currentWorkflow,
        nodes: updatedNodes,
        updatedAt: new Date().toISOString(),
      },
      selectedNode: updatedSelectedNode,
    };
  }),

  updateEdge: (edgeId, updates) => set((state) => {
    if (!state.currentWorkflow) return state;

    const updatedEdges = state.currentWorkflow.edges.map((edge) =>
      edge.id === edgeId ? { ...edge, ...updates } : edge
    );

    // Also update the selected edge if it's the one being modified
    const updatedSelectedEdge = state.selectedEdge?.id === edgeId
      ? { ...state.selectedEdge, ...updates }
      : state.selectedEdge;

    return {
      currentWorkflow: {
        ...state.currentWorkflow,
        edges: updatedEdges,
        updatedAt: new Date().toISOString(),
      },
      selectedEdge: updatedSelectedEdge,
    };
  }),

  addNode: (node) => set((state) => {
    if (!state.currentWorkflow) {
      // Create a new workflow if none exists
      return {
        currentWorkflow: {
          id: `workflow-${Date.now()}`,
          name: 'New Workflow',
          description: 'A new workflow',
          version: '1.0.0',
          nodes: [node],
          edges: [],
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        }
      };
    }
    
    return {
      currentWorkflow: {
        ...state.currentWorkflow,
        nodes: [...state.currentWorkflow.nodes, node],
        updatedAt: new Date().toISOString(),
      }
    };
  }),

  addEdge: (edge) => set((state) => ({
    currentWorkflow: state.currentWorkflow ? {
      ...state.currentWorkflow,
      edges: [...state.currentWorkflow.edges, edge],
      updatedAt: new Date().toISOString(),
    } : null
  })),

  removeNode: (nodeId) => set((state) => {
    if (!state.currentWorkflow) return state;

    // Clear selected node if it's being removed
    const newSelectedNode = state.selectedNode?.id === nodeId ? null : state.selectedNode;

    return {
      currentWorkflow: {
        ...state.currentWorkflow,
        nodes: state.currentWorkflow.nodes.filter((node) => node.id !== nodeId),
        edges: state.currentWorkflow.edges.filter(
          (edge) => edge.source !== nodeId && edge.target !== nodeId
        ),
        updatedAt: new Date().toISOString(),
      },
      selectedNode: newSelectedNode,
    };
  }),

  removeEdge: (edgeId) => set((state) => {
    if (!state.currentWorkflow) return state;

    // Clear selected edge if it's being removed
    const newSelectedEdge = state.selectedEdge?.id === edgeId ? null : state.selectedEdge;

    return {
      currentWorkflow: {
        ...state.currentWorkflow,
        edges: state.currentWorkflow.edges.filter((edge) => edge.id !== edgeId),
        updatedAt: new Date().toISOString(),
      },
      selectedEdge: newSelectedEdge,
    };
  })
}));
