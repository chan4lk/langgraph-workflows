import React, { useCallback, useEffect } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  Connection,
  Edge,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Box } from '@mui/material';
import { useWorkflowStore } from '../store/workflowStore';
import { ConfigPanel } from './panels/ConfigPanel';
import { BaseNode } from './nodes/BaseNode';
import { WorkflowNode, WorkflowEdge } from '../types/workflow';

const nodeTypes = {
  base: BaseNode,
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
      type: 'base',
      position: { x: 250, y: 50 },
      data: { label: 'Start' },
    },
    {
      id: 'agent1',
      type: 'base',
      position: { x: 250, y: 150 },
      data: { 
        label: 'Agent Node',
        agentName: 'TestAgent',
        description: 'A test agent node'
      },
    },
    {
      id: 'end',
      type: 'base',
      position: { x: 250, y: 250 },
      data: { label: 'End' },
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
    addEdge: addEdgeToStore,
  } = useWorkflowStore();

  // Set initial workflow for testing
  useEffect(() => {
    if (!currentWorkflow) {
      setCurrentWorkflow(initialWorkflow);
    }
  }, [currentWorkflow, setCurrentWorkflow]);

  const onConnect = useCallback(
    (connection: Connection) => {
      const newEdge: WorkflowEdge = {
        id: `e${connection.source}-${connection.target}`,
        source: connection.source!,
        target: connection.target!,
        type: 'default',
      };
      addEdgeToStore(newEdge);
    },
    [addEdgeToStore]
  );

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: WorkflowNode) => {
      setSelectedNode(node);
    },
    [setSelectedNode]
  );

  const onEdgeClick = useCallback(
    (_: React.MouseEvent, edge: Edge) => {
      setSelectedEdge(edge as WorkflowEdge);
    },
    [setSelectedEdge]
  );

  const onPaneClick = useCallback(() => {
    setSelectedNode(null);
    setSelectedEdge(null);
  }, [setSelectedNode, setSelectedEdge]);

  if (!currentWorkflow) {
    return null;
  }

  return (
    <Box sx={{ width: '100%', height: '100vh', bgcolor: 'background.default' }}>
      <ReactFlow
        nodes={currentWorkflow.nodes}
        edges={currentWorkflow.edges}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        onEdgeClick={onEdgeClick}
        onPaneClick={onPaneClick}
        nodeTypes={nodeTypes}
        fitView
      >
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
      <ConfigPanel />
    </Box>
  );
};
