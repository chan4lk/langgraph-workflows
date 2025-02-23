import React, { useCallback, useEffect } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  Connection,
  Edge,
  Node,
  NodeChange,
  EdgeChange,
  applyNodeChanges,
  applyEdgeChanges,
  BackgroundVariant,
  addEdge,
  MarkerType,
  useReactFlow,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Box } from '@mui/material';
import { useWorkflowStore } from '../store/workflowStore';
import { ConfigPanel } from './panels/ConfigPanel';
import { Toolbar } from './Toolbar';
import { BaseNode } from './nodes/BaseNode';
import { AgentNode } from './nodes/AgentNode';
import { HumanTaskNode } from './nodes/HumanTaskNode';
import { SubWorkflowNode } from './nodes/SubWorkflowNode';
import { WorkflowNode, WorkflowEdge, NodeType, EdgeType } from '../types/workflow';

const nodeTypes = {
  base: BaseNode,
  start: BaseNode,
  end: BaseNode,
  agent: AgentNode,
  function: BaseNode,
  human_task: HumanTaskNode,
  sub_workflow: SubWorkflowNode,
};

const defaultEdgeOptions = {
  type: 'smoothstep',
  markerEnd: {
    type: MarkerType.ArrowClosed,
    width: 20,
    height: 20,
  },
  style: {
    strokeWidth: 2,
  },
};

// Sample initial workflow for testing
const initialWorkflow = {
  id: 'test-workflow',
  name: 'Test Workflow',
  description: 'A test workflow',
  version: '1.0.0',
  nodes: [
    {
      id: 'start',
      type: 'start',
      position: { x: 250, y: 50 },
      data: { label: 'Start' },
      draggable: true,
    },
    {
      id: 'agent1',
      type: 'agent',
      position: { x: 250, y: 150 },
      data: { 
        label: 'Agent Node',
        agentName: 'TestAgent',
        description: 'A test agent node',
        llmConfigId: 'gpt-4'
      },
      draggable: true,
    },
    {
      id: 'end',
      type: 'end',
      position: { x: 250, y: 250 },
      data: { label: 'End' },
      draggable: true,
    },
  ],
  edges: [
    {
      id: 'e1-2',
      source: 'start',
      target: 'agent1',
      type: 'default',
    },
    {
      id: 'e2-3',
      source: 'agent1',
      target: 'end',
      type: 'default',
    },
  ],
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
};

export const WorkflowDesigner: React.FC = () => {
  const {
    currentWorkflow,
    setCurrentWorkflow,
    setSelectedNode,
    setSelectedEdge,
  } = useWorkflowStore();

  const { setViewport } = useReactFlow();

  // Set initial workflow for testing
  useEffect(() => {
    if (!currentWorkflow) {
      setCurrentWorkflow(initialWorkflow);
      // Center the view on the workflow
      setViewport({ x: 0, y: 0, zoom: 1.5 });
    }
  }, [currentWorkflow, setCurrentWorkflow, setViewport]);

  const onNodesChange = useCallback(
    (changes: NodeChange[]) => {
      if (!currentWorkflow?.nodes) return;

      const updatedNodes = applyNodeChanges(changes, currentWorkflow.nodes);
      setCurrentWorkflow({
        ...currentWorkflow,
        nodes: updatedNodes,
        updatedAt: new Date().toISOString(),
      });
    },
    [currentWorkflow, setCurrentWorkflow]
  );

  const onEdgesChange = useCallback(
    (changes: EdgeChange[]) => {
      if (!currentWorkflow?.edges) return;

      const updatedEdges = applyEdgeChanges(changes, currentWorkflow.edges);
      setCurrentWorkflow({
        ...currentWorkflow,
        edges: updatedEdges,
        updatedAt: new Date().toISOString(),
      });

      // If edge was removed, clear selection
      if (changes.some(change => change.type === 'remove')) {
        setSelectedEdge(null);
      }
    },
    [currentWorkflow, setCurrentWorkflow, setSelectedEdge]
  );

  const onConnect = useCallback(
    (params: Connection) => {
      if (!params.source || !params.target || !currentWorkflow) return;

      const newEdge: WorkflowEdge = {
        id: `e${params.source}-${params.target}`,
        source: params.source,
        target: params.target,
        type: 'default',
        animated: false,
        style: defaultEdgeOptions.style,
        markerEnd: defaultEdgeOptions.markerEnd,
      };

      setCurrentWorkflow({
        ...currentWorkflow,
        edges: addEdge(newEdge, currentWorkflow.edges || []),
        updatedAt: new Date().toISOString(),
      });
    },
    [currentWorkflow, setCurrentWorkflow]
  );

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: Node) => {
      // Ensure we have all the required data for the node type
      const baseData = {
        label: node.data?.label || '',
        description: node.data?.description || '',
      };

      let nodeData = { ...node.data };
      switch (node.type) {
        case 'agent':
          nodeData = {
            ...baseData,
            agentName: node.data?.agentName || '',
            llmConfigId: node.data?.llmConfigId || '',
          };
          break;
        case 'human_task':
          nodeData = {
            ...baseData,
            taskName: node.data?.taskName || '',
            assignmentRules: node.data?.assignmentRules || { users: [], groups: [] },
          };
          break;
        case 'sub_workflow':
          nodeData = {
            ...baseData,
            workflowId: node.data?.workflowId || '',
          };
          break;
        default:
          nodeData = baseData;
      }

      const workflowNode: WorkflowNode = {
        id: node.id,
        type: node.type as NodeType,
        position: node.position,
        data: nodeData,
        draggable: true,
      };

      setSelectedNode(workflowNode);
      setSelectedEdge(null);
    },
    [setSelectedNode, setSelectedEdge]
  );

  const onEdgeClick = useCallback(
    (_: React.MouseEvent, edge: Edge) => {
      setSelectedEdge(edge as WorkflowEdge);
      setSelectedNode(null);
    },
    [setSelectedNode, setSelectedEdge]
  );

  const onPaneClick = useCallback(() => {
    setSelectedNode(null);
    setSelectedEdge(null);
  }, [setSelectedNode, setSelectedEdge]);

  if (!currentWorkflow) {
    return null;
  }

  return (
    <Box sx={{ width: '100%', height: '100vh', bgcolor: 'background.default', position: 'relative' }}>
      <Toolbar />
      <ReactFlow
        nodes={currentWorkflow.nodes}
        edges={currentWorkflow.edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        onEdgeClick={onEdgeClick}
        onPaneClick={onPaneClick}
        nodeTypes={nodeTypes}
        defaultEdgeOptions={defaultEdgeOptions}
        fitView
        snapToGrid
        snapGrid={[15, 15]}
        defaultViewport={{ x: 0, y: 0, zoom: 1.5 }}
        minZoom={0.5}
        maxZoom={2}
        deleteKeyCode={['Backspace', 'Delete']}
      >
        <Background 
          variant={BackgroundVariant.Dots}
          gap={15}
          size={1}
          color="#e0e0e0"
        />
        <Controls showInteractive={false} />
        <MiniMap 
          nodeColor={(node) => {
            switch (node.type) {
              case 'start':
                return '#4caf50';
              case 'end':
                return '#f44336';
              case 'agent':
                return '#2196f3';
              case 'function':
                return '#9c27b0';
              case 'human_task':
                return '#00bcd4';
              case 'sub_workflow':
                return '#ff9800';
              default:
                return '#555';
            }
          }}
        />
      </ReactFlow>
      <ConfigPanel />
    </Box>
  );
};
