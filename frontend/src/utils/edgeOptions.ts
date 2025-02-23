import { MarkerType, EdgeOptions } from 'reactflow';

export const defaultEdgeOptions: EdgeOptions = {
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
