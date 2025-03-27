export interface PipelineSource {
  type: string;
  name: string;
  details?: Record<string, string>;
}

export interface PipelineDestination {
  type: string;
  name: string;
  path?: string;
  format?: string;
  details?: Record<string, string>;
}

export interface PipelineSchedule {
  frequency: string;
  startTime?: string;
  days?: string[];
  timezone?: string;
}

export interface PipelineExecution {
  status: 'successful' | 'failed';
  timestamp: string;
  recordsProcessed?: number;
  errorMessage?: string;
}

export interface Pipeline {
  id: string;
  name: string;
  createdOn: string;
  source: PipelineSource;
  destination: PipelineDestination;
  schedule: PipelineSchedule;
  executionHistory?: PipelineExecution[];
}
