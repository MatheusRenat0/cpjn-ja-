<template>
  <div class="page">

    <header class="site-header">
      <div class="header-inner">
        <div class="logo">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <span>Consulta <strong>CNPJ</strong></span>
        </div>
        <nav class="header-nav">
          <a href="#">Início</a>
          <a href="#">Sobre</a>
        </nav>
      </div>
    </header>

    <section class="hero" :class="{ 'hero-compact': empresa || isLoading }">
      <div class="hero-inner">
        <template v-if="!empresa && !isLoading">
          <h1 class="hero-title">Consulta de CNPJ</h1>
          <p class="hero-sub">Informe o CNPJ para obter dados cadastrais completos da empresa</p>
        </template>

        <div class="search-bar">
          <div class="search-input-wrap">
            <svg class="search-ico" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input
              v-model="cnpjInput"
              class="search-input"
              placeholder="Digite o CNPJ"
              @keyup.enter="consultar"
              @input="formatarCNPJ"
              :disabled="isLoading"
              maxlength="18"
            />
            <button v-if="cnpjInput" class="clear-btn" @click="limpar">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          <button class="btn-consultar" @click="consultar" :disabled="isLoading">
            <span v-if="isLoading" class="spinner"></span>
            <template v-else>Consultar</template>
          </button>
        </div>

        <p v-if="erro" class="search-error">
          <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          {{ erro }}
        </p>
      </div>
    </section>

    <div v-if="isLoading" class="result-wrap">
      <div class="skeleton-page">
        <div class="sk-company-head">
          <div class="sk sk-icon"></div>
          <div class="sk-texts">
            <div class="sk sk-h1"></div>
            <div class="sk sk-h2"></div>
          </div>
        </div>
        <div class="sk-divider"></div>
        <div v-for="n in 3" :key="n" class="sk-section">
          <div class="sk sk-stitle"></div>
          <div class="sk-rows">
            <div v-for="m in 4" :key="m" class="sk-row">
              <div class="sk sk-label"></div>
              <div class="sk sk-val"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="empresa && !isLoading" class="result-wrap">

      <div class="company-header">
        <div class="company-badge">{{ getIniciais(empresa.razao_social) }}</div>
        <div class="company-meta">
          <h2 class="co-name">{{ empresa.nome_fantasia || empresa.razao_social }}</h2>
          <p class="co-razao" v-if="empresa.nome_fantasia">{{ empresa.razao_social }}</p>
          <div class="co-pills">
            <span class="pill pill-cnpj">{{ empresa.cnpj }}</span>
            <span class="pill" :class="getStatusPill(empresa.descricao_situacao_cadastral)">
              <span class="pill-dot"></span>{{ empresa.descricao_situacao_cadastral }}
            </span>
            <span v-if="empresa.porte" class="pill pill-porte">{{ empresa.porte }}</span>
          </div>
        </div>
      </div>

      <div class="result-body">

        <div class="data-section">
          <h3 class="section-title">
            <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 9h6M9 13h4"/></svg>
            Dados Cadastrais
          </h3>
          <div class="data-table">
            <div class="data-row"><span class="dr-label">Razão Social</span><span class="dr-val">{{ empresa.razao_social || '—' }}</span></div>
            <div class="data-row"><span class="dr-label">Nome Fantasia</span><span class="dr-val">{{ empresa.nome_fantasia || '—' }}</span></div>
            <div class="data-row"><span class="dr-label">CNPJ</span><span class="dr-val mono">{{ empresa.cnpj }}</span></div>
            <div class="data-row"><span class="dr-label">Natureza Jurídica</span><span class="dr-val">{{ empresa.natureza_juridica || '—' }}</span></div>
            <div class="data-row"><span class="dr-label">Porte</span><span class="dr-val">{{ empresa.porte || '—' }}</span></div>
            <div class="data-row"><span class="dr-label">Capital Social</span><span class="dr-val">{{ formatarMoeda(empresa.capital_social) }}</span></div>
            <div class="data-row"><span class="dr-label">Data de Abertura</span><span class="dr-val">{{ formatarData(empresa.data_inicio_atividade) }}</span></div>
            <div class="data-row">
              <span class="dr-label">Situação</span>
              <span class="dr-val">
                <span class="inline-status" :class="getStatusPill(empresa.descricao_situacao_cadastral)">
                  <span class="pill-dot"></span>{{ empresa.descricao_situacao_cadastral }}
                </span>
              </span>
            </div>
            <div class="data-row" v-if="empresa.data_situacao_cadastral"><span class="dr-label">Data da Situação</span><span class="dr-val">{{ formatarData(empresa.data_situacao_cadastral) }}</span></div>
            <div class="data-row" v-if="empresa.motivo_situacao_cadastral"><span class="dr-label">Motivo</span><span class="dr-val">{{ empresa.motivo_situacao_cadastral }}</span></div>
          </div>
        </div>

        <div class="two-col">
          <div class="data-section">
            <h3 class="section-title">
              <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              Endereço
            </h3>
            <div class="data-table">
              <div class="data-row"><span class="dr-label">Logradouro</span><span class="dr-val">{{ empresa.logradouro || '—' }}, {{ empresa.numero || 'S/N' }}</span></div>
              <div class="data-row" v-if="empresa.complemento"><span class="dr-label">Complemento</span><span class="dr-val">{{ empresa.complemento }}</span></div>
              <div class="data-row"><span class="dr-label">Bairro</span><span class="dr-val">{{ empresa.bairro || '—' }}</span></div>
              <div class="data-row"><span class="dr-label">Município / UF</span><span class="dr-val">{{ empresa.municipio || '—' }} / {{ empresa.uf || '—' }}</span></div>
              <div class="data-row"><span class="dr-label">CEP</span><span class="dr-val mono">{{ empresa.cep || '—' }}</span></div>
            </div>
          </div>

          <div class="data-section">
            <h3 class="section-title">
              <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.77 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 17.18z"/></svg>
              Contato
            </h3>
            <div class="data-table">
              <div class="data-row"><span class="dr-label">Telefone 1</span><span class="dr-val mono">{{ formatTel(empresa.ddd_telefone_1, empresa.telefone_1) }}</span></div>
              <div class="data-row" v-if="empresa.ddd_telefone_2"><span class="dr-label">Telefone 2</span><span class="dr-val mono">{{ formatTel(empresa.ddd_telefone_2, empresa.telefone_2) }}</span></div>
              <div class="data-row"><span class="dr-label">E-mail</span><span class="dr-val">{{ empresa.email || '—' }}</span></div>
            </div>
            
            <template v-if="empresa.qsa && empresa.qsa.length">
              <h3 class="section-title" style="margin-top:1px">
                <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
                Quadro Societário
              </h3>
              <div class="socio-list">
                <div v-for="s in empresa.qsa" :key="s.nome_socio" class="socio-item">
                  <div class="socio-avatar">{{ s.nome_socio?.[0] }}</div>
                  <div class="socio-info">
                    <p class="socio-name">{{ s.nome_socio }}</p>
                    <p class="socio-qual">{{ s.qualificacao_socio }}</p>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>
        
        <div class="data-section" v-if="empresa.cnae_fiscal">
          <h3 class="section-title">
            <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
            Atividade Econômica (CNAE)
          </h3>
          <div class="cnae-block primary-cnae">
            <span class="cnae-badge">PRINCIPAL</span>
            <div class="cnae-info">
              <code class="cnae-code">{{ empresa.cnae_fiscal }}</code>
              <span class="cnae-desc">{{ empresa.cnae_fiscal_descricao || '—' }}</span>
            </div>
          </div>
          <template v-if="empresa.cnaes_secundarios && empresa.cnaes_secundarios.length">
            <p class="secondary-label">Secundárias ({{ empresa.cnaes_secundarios.length }})</p>
            <div v-for="cnae in empresa.cnaes_secundarios" :key="cnae.codigo" class="cnae-block secondary-cnae">
              <div class="cnae-info">
                <code class="cnae-code">{{ cnae.codigo }}</code>
                <span class="cnae-desc">{{ cnae.descricao }}</span>
              </div>
            </div>
          </template>
        </div>

      </div>

      <div class="result-footer">
        <span>Dados obtidos via Receita Federal do Brasil</span>
        <button class="btn-export" @click="exportar">
          <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          Exportar JSON
        </button>
      </div>
    </div>

    <footer class="site-footer">
      <p>Consulta CNPJ — Dados da Receita Federal do Brasil</p>
    </footer>

  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'ConsultaCNPJ',
  data() {
    return {
      cnpjInput: '',
      empresa: null,
      isLoading: false,
      erro: null,
    };
  },
  methods: {
    async consultar() {
      const limpo = this.cnpjInput.replace(/\D/g, '');
      if (!limpo) { this.erro = 'Informe um CNPJ válido.'; return; }
      if (limpo.length !== 14) { this.erro = 'O CNPJ deve ter 14 dígitos.'; return; }
      this.isLoading = true;
      this.erro = null;
      this.empresa = null;
      try {
        const { data } = await api.get(`/cnpj/${limpo}`);
        this.empresa = data;
      } catch (err) {
        this.erro = err.response?.data?.erro || 'Erro ao conectar com o servidor.';
      } finally {
        this.isLoading = false;
      }
    },

    formatarCNPJ(e) {
      let v = e.target.value.replace(/\D/g, '');
      v = v.replace(/^(\d{2})(\d)/, '$1.$2');
      v = v.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
      v = v.replace(/\.(\d{3})(\d)/, '.$1/$2');
      v = v.replace(/(\d{4})(\d)/, '$1-$2');
      this.cnpjInput = v;
      this.erro = null;
    },

    limpar() { this.cnpjInput = ''; this.empresa = null; this.erro = null; },

    getIniciais(n) {
      if (!n) return 'EM';
      return n.trim().split(/\s+/).slice(0, 2).map(w => w[0]).join('').toUpperCase();
    },

    getStatusPill(s) {
      if (!s) return '';
      const l = s.toLowerCase();
      if (l.includes('ativa')) return 'pill-ativa';
      if (l.includes('suspend') || l.includes('inapta')) return 'pill-suspensa';
      if (l.includes('baixada') || l.includes('cancelada')) return 'pill-baixada';
      return 'pill-outro';
    },

    formatarData(d) {
      if (!d) return '—';
      try {
        const iso = d.includes('-') ? d : `${d.slice(0,4)}-${d.slice(4,6)}-${d.slice(6,8)}`;
        return new Date(iso + 'T00:00:00').toLocaleDateString('pt-BR');
      } catch { return d; }
    },

    formatarMoeda(v) {
      if (!v) return '—';
      return Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    },

    formatTel(ddd, tel) {
      if (!ddd && !tel) return '—';
      return `(${ddd || ''}) ${tel || ''}`.trim();
    },

    exportar() {
      const blob = new Blob([JSON.stringify(this.empresa, null, 2)], { type: 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `cnpj_${this.empresa.cnpj?.replace(/\D/g,'')}.json`;
      a.click();
    }
  }
};
</script>