import React, { useCallback, useEffect, useState } from 'react';
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
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Box } from '@mui/material';
import { useWorkflowStore } from '../store/workflowStore';
import { ConfigPanel } from './panels/ConfigPanel';
import { Toolbar } from './Toolbar';
import { NodeConfiguration } from './NodeConfiguration';
import { Workflow, WorkflowNode, WorkflowEdge, NodeType, EdgeTypes, NodeData, NodeTool } from '../types/workflow';
import { Tool } from '../types/tool';
import { nodeTypes } from '../utils/nodeTypes';
import { defaultEdgeOptions } from '../utils/edgeOptions';
import { getNodeColor } from '../utils/nodeColors';
import { workflowApi } from '../api/workflowApi';

// Sample initial workflow for testing
const initialWorkflow: Workflow = {
  id: 'test-workflow',
  name: 'Test Workflow',
  description: 'A test workflow',
  version: '1.0.0',
  nodes: [
    {
      id: 'start',
      type: NodeType.START,
      position: { x: 250, y: 50 },
      data: { 
        label: 'Start',
        type: NodeType.START
      },
      draggable: true,
    },
    {
      id: 'agent1',
      type: NodeType.AGENT,
      position: { x: 250, y: 150 },
      data: { 
        label: 'Agent Node',
        type: NodeType.AGENT,
        agentName: 'TestAgent',
        description: 'A test agent node',
        llmConfigId: 'gpt-4'
      },
      draggable: true,
    },
    {
      id: 'end',
      type: NodeType.END,
      position: { x: 250, y: 250 },
      data: { 
        label: 'End',
        type: NodeType.END
      },
      draggable: true,
    },
  ] as WorkflowNode[],
  edges: [
    {
      id: 'e1-2',
      source: 'start',
      target: 'agent1',
      type: 'default' as EdgeTypes,
    },
    {
      id: 'e2-3',
      source: 'agent1',
      target: 'end',
      type: 'default' as EdgeTypes,
    },
  ] as WorkflowEdge[],
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
};

export const WorkflowDesigner: React.FC = () => {
  const { 
    currentWorkflow, 
    setCurrentWorkflow,
    selectedNode: storeSelectedNode,
    setSelectedNode: setStoreSelectedNode,
    setSelectedEdge 
  } = useWorkflowStore();
  const [configOpen, setConfigOpen] = useState(false);
  const [tools, setTools] = useState<Tool[]>([]);

  useEffect(() => {
    // Load tools on component mount
    const fetchTools = async () => {
      try {
        const toolsData = await workflowApi.getTools();
        setTools(toolsData);
      } catch (error) {
        console.error('Failed to load tools:', error);
      }
    };

    fetchTools();
  }, []);

  useEffect(() => {
    if (!currentWorkflow) {
      setCurrentWorkflow(initialWorkflow);
    }
  }, [currentWorkflow, setCurrentWorkflow]);

  const onNodesChange = useCallback(
    (changes: NodeChange[]) => {
      if (!currentWorkflow) return;
      setCurrentWorkflow({
        ...currentWorkflow,
        nodes: applyNodeChanges(changes, currentWorkflow.nodes),
        updatedAt: new Date().toISOString(),
      });
    },
    [currentWorkflow, setCurrentWorkflow]
  );

  const onEdgesChange = useCallback(
    (changes: EdgeChange[]) => {
      if (!currentWorkflow) return;
      const newEdges = applyEdgeChanges(changes, currentWorkflow.edges) as WorkflowEdge[];
      setCurrentWorkflow({
        ...currentWorkflow,
        edges: newEdges,
        updatedAt: new Date().toISOString(),
      });
    },
    [currentWorkflow, setCurrentWorkflow]
  );

  const onConnect = useCallback(
    (connection: Connection) => {
      if (!currentWorkflow || !connection.source || !connection.target) return;
      
      const newEdge: WorkflowEdge = {
        id: `e${connection.source}-${connection.target}`,
        source: connection.source,
        target: connection.target,
        type: 'smoothstep',
        data: {}
      };

      // Only add handles if they are present
      if (connection.sourceHandle) {
        newEdge.sourceHandle = connection.sourceHandle;
      }
      if (connection.targetHandle) {
        newEdge.targetHandle = connection.targetHandle;
      }

      setCurrentWorkflow({
        ...currentWorkflow,
        edges: [...currentWorkflow.edges, newEdge],
        updatedAt: new Date().toISOString(),
      });
    },
    [currentWorkflow, setCurrentWorkflow]
  );

  const onNodeClick = useCallback((_: React.MouseEvent, node: Node) => {
    const workflowNode = node as WorkflowNode;
    setStoreSelectedNode(workflowNode);
    // Only open NodeConfiguration for specific node types that need it
    if (workflowNode.data.type === NodeType.TOOL || workflowNode.data.type === NodeType.AGENT) {
      setConfigOpen(true);
    }
  }, [setStoreSelectedNode, setSelectedEdge]);

  const onPaneClick = useCallback(() => {
    setStoreSelectedNode(null);
    setSelectedEdge(null);
    setConfigOpen(false);
  }, [setStoreSelectedNode, setSelectedEdge]);

  const handleConfigClose = useCallback(() => {
    setConfigOpen(false);
  }, []);

  const handleConfigSave = useCallback((updates: Partial<NodeData>) => {
    if (!currentWorkflow || !storeSelectedNode) return;

    setCurrentWorkflow({
      ...currentWorkflow,
      nodes: currentWorkflow.nodes.map((node) =>
        node.id === storeSelectedNode.id
          ? { ...node, data: { ...node.data, ...updates } }
          : node
      ),
      updatedAt: new Date().toISOString(),
    });

    setConfigOpen(false);
  }, [currentWorkflow, storeSelectedNode, setCurrentWorkflow]);

  const handleToolsUpdate = useCallback((nodeId: string, tools: NodeTool[]) => {
    if (!currentWorkflow || !storeSelectedNode) return;

    setCurrentWorkflow({
      ...currentWorkflow,
      nodes: currentWorkflow.nodes.map((node) =>
        node.id === nodeId
          ? { ...node, data: { ...node.data, tools } }
          : node
      ),
      updatedAt: new Date().toISOString(),
    });
  }, [currentWorkflow, storeSelectedNode, setCurrentWorkflow]);

  const onEdgeClick = useCallback((_: React.MouseEvent, edge: Edge) => {
    setStoreSelectedNode(null);
    const workflowEdge: WorkflowEdge = {
      id: edge.id,
      source: edge.source,
      target: edge.target,
      type: edge.type as EdgeTypes || 'default',
      sourceHandle: edge.sourceHandle || undefined,
      targetHandle: edge.targetHandle || undefined,
      data: edge.data || {}
    };
    setSelectedEdge(workflowEdge);
  }, [setStoreSelectedNode, setSelectedEdge]);

  return (
    <Box sx={{ width: '100%', height: '100vh', position: 'relative' }}>
      <Toolbar />
      <ReactFlow
        nodes={currentWorkflow?.nodes || []}
        edges={currentWorkflow?.edges || []}
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
          nodeColor={(node) => getNodeColor(node.type as NodeType)}
        />
        <Box
          sx={{
            position: 'absolute',
            right: 10,
            top: 10,
            zIndex: 4,
            backgroundColor: 'white',
            borderRadius: 1,
            boxShadow: 1,
            width: 300,
          }}
        >
          <ConfigPanel />
        </Box>
      </ReactFlow>
      {storeSelectedNode && (
        <NodeConfiguration
          open={configOpen}
          node={storeSelectedNode.data}
          onClose={handleConfigClose}
          onSave={handleConfigSave}
          onToolsUpdate={handleToolsUpdate}
          tools={tools}
        />
      )}
    </Box>
  );
};
