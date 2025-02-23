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

export const useWorkflowStore = create<WorkflowState>((set, get) => ({
  workflows: [],
  currentWorkflow: null,
  selectedNode: null,
  selectedEdge: null,

  setWorkflows: (workflows) => set({ workflows }),
  
  setCurrentWorkflow: (workflow) => {
    console.log('Setting current workflow:', workflow);
    set({ 
      currentWorkflow: workflow,
      selectedNode: null,
      selectedEdge: null
    });
  },

  setSelectedNode: (node) => {
    console.log('Setting selected node:', node);
    console.log('Previous state:', get());
    set((state) => ({
      ...state,
      selectedNode: node,
      selectedEdge: null
    }));
    console.log('New state:', get());
  },

  setSelectedEdge: (edge) => {
    console.log('Setting selected edge:', edge);
    set((state) => ({
      ...state,
      selectedEdge: edge,
      selectedNode: null
    }));
  },

  updateNode: (nodeId, updates) => {
    console.log('Updating node:', nodeId, updates);
    set((state) => {
      if (!state.currentWorkflow) return state;

      const updatedNodes = state.currentWorkflow.nodes.map((node) =>
        node.id === nodeId ? { ...node, ...updates } : node
      );

      return {
        ...state,
        currentWorkflow: {
          ...state.currentWorkflow,
          nodes: updatedNodes,
          updatedAt: new Date().toISOString(),
        },
      };
    });
  },

  updateEdge: (edgeId, updates) => set((state) => {
    if (!state.currentWorkflow) return state;

    const updatedEdges = state.currentWorkflow.edges.map((edge) =>
      edge.id === edgeId ? { ...edge, ...updates } : edge
    );

    return {
      ...state,
      currentWorkflow: {
        ...state.currentWorkflow,
        edges: updatedEdges,
        updatedAt: new Date().toISOString(),
      },
    };
  }),

  addNode: (node) => set((state) => {
    if (!state.currentWorkflow) return state;

    return {
      ...state,
      currentWorkflow: {
        ...state.currentWorkflow,
        nodes: [...state.currentWorkflow.nodes, node],
        updatedAt: new Date().toISOString(),
      },
    };
  }),

  addEdge: (edge) => set((state) => {
    if (!state.currentWorkflow) return state;

    return {
      ...state,
      currentWorkflow: {
        ...state.currentWorkflow,
        edges: [...state.currentWorkflow.edges, edge],
        updatedAt: new Date().toISOString(),
      },
    };
  }),

  removeNode: (nodeId) => set((state) => {
    if (!state.currentWorkflow) return state;

    return {
      ...state,
      currentWorkflow: {
        ...state.currentWorkflow,
        nodes: state.currentWorkflow.nodes.filter((node) => node.id !== nodeId),
        edges: state.currentWorkflow.edges.filter(
          (edge) => edge.source !== nodeId && edge.target !== nodeId
        ),
        updatedAt: new Date().toISOString(),
      },
    };
  }),

  removeEdge: (edgeId) => set((state) => {
    if (!state.currentWorkflow) return state;

    return {
      ...state,
      currentWorkflow: {
        ...state.currentWorkflow,
        edges: state.currentWorkflow.edges.filter((edge) => edge.id !== edgeId),
        updatedAt: new Date().toISOString(),
      },
    };
  }),
}));
