/**
 * TypeScript Type Definitions (`src/frontend/src/types/index.ts`).
 *
 * All interface property names MUST use uniform snake_case matching Backend Pydantic schemas.
 */

export interface BaseEntity {
  id: string;
  created_at?: string;
  updated_at?: string;
}
