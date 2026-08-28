/**
 * A dependency-free teaching analogue of Service/Event/Effect lifecycles.
 *
 * This is intentionally not presented as the current DeepSeek Harness API.
 * After pinning a repository commit, map these invariants onto its official
 * Cordis tutorial and replace the adapter in your experiment branch.
 */

type Disposer = () => void;
type Listener = (payload: unknown) => void;

class TeachingContext {
  private services = new Map<string, unknown>();
  private listeners = new Map<string, Set<Listener>>();
  private effects: Disposer[] = [];

  provide(name: string, service: unknown): void {
    if (this.services.has(name)) throw new Error(`duplicate service: ${name}`);
    this.services.set(name, service);
    this.effects.push(() => this.services.delete(name));
  }

  on(event: string, listener: Listener): void {
    const bucket = this.listeners.get(event) ?? new Set<Listener>();
    bucket.add(listener);
    this.listeners.set(event, bucket);
    this.effects.push(() => bucket.delete(listener));
  }

  emit(event: string, payload: unknown): void {
    for (const listener of this.listeners.get(event) ?? []) listener(payload);
  }

  dispose(): void {
    for (const cleanup of this.effects.reverse()) cleanup();
    this.effects = [];
  }

  snapshot(): { services: number; listeners: number } {
    return {
      services: this.services.size,
      listeners: [...this.listeners.values()].reduce((n, set) => n + set.size, 0),
    };
  }
}

function installGreetingPlugin(ctx: TeachingContext): void {
  ctx.provide("greet", (name: string) => `hello, ${name}`);
  ctx.on("tool:before", (payload) => console.log("policy observed", payload));
}

const ctx = new TeachingContext();
installGreetingPlugin(ctx);
console.log("installed", ctx.snapshot());
ctx.emit("tool:before", { tool: "greet", risk: "read" });
ctx.dispose();
console.log("disposed", ctx.snapshot());
