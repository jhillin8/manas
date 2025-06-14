// Utility function for className concatenation (shadcn/ui style)
export function cn(...args: any[]): string {
  return args.filter(Boolean).join(' ');
}
