import { createClient } from '@supabase/supabase-js';

// The user mentioned they put the keys in the .env file.
// In Vite, these must be prefixed with VITE_ to be accessible in the browser.
// We will fallback to process.env just in case, but Vite uses import.meta.env
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://placeholder.supabase.co';
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'placeholder_key';

export const supabase = createClient(supabaseUrl, supabaseKey);
