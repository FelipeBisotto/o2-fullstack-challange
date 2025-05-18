import { z } from 'zod';

export const tipoMovimentacaoEnum = z.enum(['entrada', 'saida'], {
  required_error: 'O tipo da movimentação é obrigatório.',
});

export const movimentacaoFormSchema = z.object({
  produto_id: z
    .union([z.string().regex(/^\d+$/, 'Produto inválido'), z.number()])
    .transform((val) => typeof val === 'string' ? parseInt(val, 10) : val)
    .refine((val) => val > 0, { message: 'Produto inválido.' }),

  tipo: tipoMovimentacaoEnum,

  quantidade: z
    .number({ invalid_type_error: 'Informe um número válido.' })
    .int('A quantidade deve ser um número inteiro.')
    .positive('A quantidade deve ser maior que zero.'),
});

export type MovimentacaoFormData = z.infer<typeof movimentacaoFormSchema>;

export interface Movimentacao extends MovimentacaoFormData {
  id: number;
  data: string; // ISO date
  produto_nome?: string;
}

export type MovimentacaoFormState = {
  produto_id: string;
  tipo: 'entrada' | 'saida';
  quantidade: number;
};
