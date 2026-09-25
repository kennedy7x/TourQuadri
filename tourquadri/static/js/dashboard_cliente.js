// ========================================
// TOURQUADRI - Dashboard do Cliente (Estatísticas)
// ========================================

// Paleta de cores da marca
var CORES = {
    azul: 'rgba(37, 99, 235, 1)',
    laranja: 'rgba(244, 162, 97, 1)',
    verde: 'rgba(16, 185, 129, 1)',
    vermelho: 'rgba(239, 68, 68, 1)',
    amarelo: 'rgba(245, 158, 11, 1)',
    roxo: 'rgba(168, 85, 247, 1)',
    ciano: 'rgba(20, 184, 166, 1)',
    azulClaro: 'rgba(139, 184, 255, 1)'
};

// Configuração global do Chart.js
if (typeof Chart !== 'undefined') {
    Chart.defaults.font.family = "'Segoe UI', Arial, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.color = '#6b7280';
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(17, 24, 39, 0.95)';
    Chart.defaults.plugins.tooltip.padding = 12;
    Chart.defaults.plugins.tooltip.cornerRadius = 8;
    Chart.defaults.plugins.tooltip.titleFont = { size: 13, weight: '600' };
    Chart.defaults.plugins.tooltip.bodyFont = { size: 12 };
    Chart.defaults.plugins.tooltip.displayColors = true;
    Chart.defaults.plugins.tooltip.boxPadding = 6;
}

document.addEventListener('DOMContentLoaded', function() {
    carregarDashboardCliente();
});

function carregarDashboardCliente() {
    fetch('/api/dashboard_cliente')
        .then(function(response) { return response.json(); })
        .then(function(dados) {
            // Preenche cards de resumo
            var elTotal = document.getElementById('estTotalPasseios');
            if (elTotal) elTotal.textContent = dados.total_passeios || 0;

            var elFin = document.getElementById('estFinalizados');
            if (elFin) elFin.textContent = dados.total_finalizado || 0;

            var elAg = document.getElementById('estAgendados');
            if (elAg) elAg.textContent = dados.total_agendado || 0;

            var elCan = document.getElementById('estCancelados');
            if (elCan) elCan.textContent = dados.total_cancelado || 0;

            // Renderiza gráficos
            renderizarGraficoMeses(dados);
            renderizarGraficoRoteiros(dados);
            renderizarGraficoStatus(dados);
        })
        .catch(function(erro) {
            console.error('Erro ao carregar dashboard do cliente:', erro);
        });
}

// ========================================
// GRÁFICO DE LINHA — Passeios por mês
// ========================================
function renderizarGraficoMeses(dados) {
    var ctx = document.getElementById('graficoClienteMeses');
    if (!ctx) return;

    var gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 280);
    gradient.addColorStop(0, 'rgba(37, 99, 235, 0.35)');
    gradient.addColorStop(1, 'rgba(37, 99, 235, 0.02)');

    new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: dados.meses_labels,
            datasets: [{
                label: 'Passeios',
                data: dados.meses_dados,
                borderColor: CORES.azul,
                backgroundColor: gradient,
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#fff',
                pointBorderColor: CORES.azul,
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 8,
                pointHoverBackgroundColor: CORES.azul,
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            var v = context.parsed.y;
                            return ' ' + v + (v === 1 ? ' passeio' : ' passeios');
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 1, precision: 0, color: '#9ca3af' },
                    grid: { color: 'rgba(229, 231, 235, 0.6)', drawBorder: false }
                },
                x: {
                    ticks: { color: '#9ca3af' },
                    grid: { display: false }
                }
            }
        }
    });
}

// ========================================
// GRÁFICO DONUT — Roteiros que mais fez
// ========================================
function renderizarGraficoRoteiros(dados) {
    var ctx = document.getElementById('graficoClienteRoteiros');
    if (!ctx) return;

    if (!dados.roteiros_labels || dados.roteiros_labels.length === 0) {
        ctx.parentElement.innerHTML = '<p class="text-muted text-center" style="padding: 60px 0;"><i class="fas fa-inbox" style="font-size: 32px; opacity: 0.3; display: block; margin-bottom: 10px;"></i>Nenhum passeio realizado ainda.</p>';
        return;
    }

    var cores = [
        CORES.azul,
        CORES.laranja,
        CORES.verde,
        CORES.vermelho,
        CORES.azulClaro,
        CORES.roxo,
        CORES.amarelo,
        CORES.ciano
    ];

    new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: dados.roteiros_labels,
            datasets: [{
                data: dados.roteiros_dados,
                backgroundColor: cores,
                borderWidth: 3,
                borderColor: '#fff',
                hoverOffset: 10,
                hoverBorderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 10,
                        boxHeight: 10,
                        padding: 12,
                        font: { size: 11 },
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            var total = context.dataset.data.reduce(function(a, b) { return a + b; }, 0);
                            var valor = context.parsed;
                            var pct = total > 0 ? ((valor / total) * 100).toFixed(1) : 0;
                            return ' ' + valor + ' (' + pct + '%)';
                        }
                    }
                }
            }
        }
    });
}

// ========================================
// GRÁFICO DONUT — Status dos passeios
// ========================================
function renderizarGraficoStatus(dados) {
    var ctx = document.getElementById('graficoClienteStatus');
    if (!ctx) return;

    var labels = [];
    var valores = [];
    var cores = [];

    if (dados.total_agendado > 0) {
        labels.push('Agendado');
        valores.push(dados.total_agendado);
        cores.push(CORES.azul);
    }
    if (dados.total_em_andamento > 0) {
        labels.push('Em Andamento');
        valores.push(dados.total_em_andamento);
        cores.push(CORES.amarelo);
    }
    if (dados.total_finalizado > 0) {
        labels.push('Finalizado');
        valores.push(dados.total_finalizado);
        cores.push(CORES.verde);
    }
    if (dados.total_cancelado > 0) {
        labels.push('Cancelado');
        valores.push(dados.total_cancelado);
        cores.push(CORES.vermelho);
    }

    if (labels.length === 0) {
        ctx.parentElement.innerHTML = '<p class="text-muted text-center" style="padding: 60px 0;"><i class="fas fa-chart-pie" style="font-size: 32px; opacity: 0.3; display: block; margin-bottom: 10px;"></i>Nenhum passeio registrado.</p>';
        return;
    }

    new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: valores,
                backgroundColor: cores,
                borderWidth: 3,
                borderColor: '#fff',
                hoverOffset: 10,
                hoverBorderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 10,
                        boxHeight: 10,
                        padding: 12,
                        font: { size: 11 },
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            var total = context.dataset.data.reduce(function(a, b) { return a + b; }, 0);
                            var valor = context.parsed;
                            var pct = total > 0 ? ((valor / total) * 100).toFixed(1) : 0;
                            return ' ' + valor + ' (' + pct + '%)';
                        }
                    }
                }
            }
        }
    });
}