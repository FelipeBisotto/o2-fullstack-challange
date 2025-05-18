import { z } from 'zod';

export const produtoFormSchema = z.object({
  nome: z.string()
    .min(2, 'Nome é obrigatório e deve ter no mínimo 2 caracteres')
    .max(255, 'Nome não pode ultrapassar 255 caracteres'),

  descricao: z.string()
    .max(1000, 'Descrição não pode ultrapassar 1000 caracteres')
    .optional(),

  categoria: z.string()
    .min(1, 'Categoria é obrigatória')
    .max(255, 'Categoria não pode ultrapassar 255 caracteres'),

  preco_unitario: z
    .string()
    .transform((val) => parseFloat(val.replace(',', '.')))
    .refine((val) => !isNaN(val) && val > 0, {
      message: 'Preço deve ser um número positivo válido',
    }),

  quantidade: z
    .string()
    .transform((val) => parseInt(val))
    .refine((val) => Number.isInteger(val) && val > 0, {
      message: 'Quantidade deve ser um número inteiro maior que zero',
    }),
});

export type ProdutoFormSchemaData = z.infer<typeof produtoFormSchema>;

export interface ProdutoFormDataManual {
  nome: string;
  descricao?: string;
  categoria: string;
  preco_unitario: string;
  quantidade: string;
}

export interface Produto extends ProdutoFormSchemaData {
  id: number;
}
