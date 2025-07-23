type Callback<T> = (data: T) => void;

class WebSocketClient {
  private socket: WebSocket | null = null;
  private callbacks: Map<string, Set<Callback<any>>> = new Map();
  private url: string;
  private reconnectInterval: number = 5000;
  private reconnectTimeout: any;

  constructor(url: string) {
    this.url = url;
    this.connect();
  }

  private connect() {
    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      console.log('WebSocket connected');
      if (this.reconnectTimeout) {
        clearTimeout(this.reconnectTimeout);
        this.reconnectTimeout = null;
      }
    };

    this.socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        const { action, data } = message;
        if (action && this.callbacks.has(action)) {
          this.callbacks.get(action)!.forEach(cb => cb(data));
        }
      } catch (err) {
        console.error('Failed to parse WebSocket message', err);
      }
    };

    this.socket.onclose = () => {
      console.log('WebSocket disconnected, attempting to reconnect...');
      this.reconnectTimeout = setTimeout(() => this.connect(), this.reconnectInterval);
    };

    this.socket.onerror = (err) => {
      console.error('WebSocket error', err);
      this.socket?.close();
    };
  }

  send<T>(msg: T) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(msg));
    } else {
      console.warn('WebSocket not connected, message not sent');
    }
  }

  on<T>(action: string, cb: Callback<T>): () => void {
    if (!this.callbacks.has(action)) {
      this.callbacks.set(action, new Set());
    }
    this.callbacks.get(action)!.add(cb);

    return () => {
      this.callbacks.get(action)!.delete(cb);
      if (this.callbacks.get(action)!.size === 0) {
        this.callbacks.delete(action);
      }
    };
  }
}

const WS = new WebSocketClient(`wss://${window.location.host}/v1`);

export { WS };
