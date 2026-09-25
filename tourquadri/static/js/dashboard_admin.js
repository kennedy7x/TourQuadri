// ========================================
// TOURQUADRI - Dashboard Admin (Visão Geral)
// ========================================

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

window.onload = function() {
    console.log('📊 Carregando dashboard admin...');
    carregarDashboardAdmin();
};

function carregarDashboardAdmin() {
    fetch('/api/dashboard_admin')
        .then(function(response) { return response.json(); })
        .then(function(dados) {
            console.log('📊 Dados recebidos:', dados);

            renderizarGraficoDias(dados);
            renderizarGraficoRoteirosAdmin(dados);
            renderizarGraficoHorarios(dados);
            renderizarGraficoMaquinas(dados);
        })
        .catch(function(erro) {
            console.error('❌ Erro ao carregar dashboard admin:', erro);
        });
}

// ========================================
// GRÁFICO DE LINHA — Agendamentos por dia
// ========================================
function renderizarGraficoDias(dados) {
    var ctx = document.getElementById('graficoAdminDias');
    if (!ctx) {
        console.warn('⚠️ Canvas graficoAdminDias não encontrado');
        return;
    }

    var gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 280);
    gradient.addColorStop(0, 'rgba(37, 99, 235, 0.35)');
    gradient.addColorStop(1, 'rgba(37, 99, 235, 0.02)');

    new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: dados.dias_labels,
            datasets: [{
                label: 'Agendamentos',
                data: dados.dias_dados,
                borderColor: CORES.azul,
                backgroundColor: gradient,
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#fff',
                pointBorderColor: CORES.azul,
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { intersect: false, mode: 'index' },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            var v = context.parsed.y;
                            return ' ' + v + (v === 1 ? ' agendamento' : ' agendamentos');
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
                    ticks: {
                        maxRotation: 45,
                        minRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 10,
                        color: '#9ca3af'
                    },
                    grid: { display: false }
                }
            }
        }
    });
}

// ========================================
// GRÁFICO DONUT — Roteiros mais procurados
// ========================================
function renderizarGraficoRoteirosAdmin(dados) {
    var ctx = document.getElementById('graficoAdminRoteiros');
    if (!ctx) {
        console.warn('⚠️ Canvas graficoAdminRoteiros não encontrado');
        return;
    }

    if (!dados.roteiros_labels || dados.roteiros_labels.length === 0) {
        ctx.parentElement.innerHTML = '<p class="text-muted text-center" style="padding: 60px 0;"><i class="fas fa-inbox" style="font-size: 32px; opacity: 0.3; display: block; margin-bottom: 10px;"></i>Nenhum agendamento ainda.</p>';
        return;
    }

    var cores = [CORES.azul, CORES.laranja, CORES.verde, CORES.vermelho,
                 CORES.azulClaro, CORES.roxo, CORES.amarelo, CORES.ciano];

    new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: dados.roteiros_labels,
            datasets: [{
                data: dados.roteiros_dados,
                backgroundColor: cores,
                borderWidth: 3,
                borderColor: '#fff',
                hoverOffset: 10
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
                        boxWidth: 10, boxHeight: 10, padding: 12,
                        font: { size: 11 }, usePointStyle: true, pointStyle: 'circle'
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
// GRÁFICO DE BARRAS — Horários mais procurados
// ========================================
function renderizarGraficoHorarios(dados) {
    var ctx = document.getElementById('graficoAdminHorarios');
    if (!ctx) {
        console.warn('⚠️ Canvas graficoAdminHorarios não encontrado');
        return;
    }

    if (!dados.horarios_labels || dados.horarios_labels.length === 0) {
        ctx.parentElement.innerHTML = '<p class="text-muted text-center" style="padding: 60px 0;"><i class="fas fa-clock" style="font-size: 32px; opacity: 0.3; display: block; margin-bottom: 10px;"></i>Nenhum agendamento ainda.</p>';
        return;
    }

    var gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 280);
    gradient.addColorStop(0, 'rgba(37, 99, 235, 0.9)');
    gradient.addColorStop(1, 'rgba(139, 184, 255, 0.6)');

    new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: dados.horarios_labels,
            datasets: [{
                label: 'Agendamentos',
                data: dados.horarios_dados,
                backgroundColor: gradient,
                borderColor: CORES.azul,
                borderWidth: 0,
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            var v = context.parsed.y;
                            return ' ' + v + (v === 1 ? ' agendamento' : ' agendamentos');
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
                    ticks: {
                        color: '#9ca3af', maxRotation: 45, minRotation: 0,
                        autoSkip: true, maxTicksLimit: 12, font: { size: 10 }
                    },
                    grid: { display: false }
                }
            }
        }
    });
}

// ========================================
// GRÁFICO DE BARRAS — Top 10 máquinas
// ========================================
function renderizarGraficoMaquinas(dados) {
    var ctx = document.getElementById('graficoAdminMaquinas');
    if (!ctx) {
        console.warn('⚠️ Canvas graficoAdminMaquinas não encontrado');
        return;
    }

    if (!dados.maquinas_labels || dados.maquinas_labels.length === 0) {
        ctx.parentElement.innerHTML = '<p class="text-muted text-center" style="padding: 60px 0;"><i class="fas fa-tractor" style="font-size: 32px; opacity: 0.3; display: block; margin-bottom: 10px;"></i>Nenhuma máquina foi usada ainda.</p>';
        return;
    }

    var gradient = ctx.getContext('2d').createLinearGradient(0, 0, 600, 0);
    gradient.addColorStop(0, 'rgba(37, 99, 235, 0.9)');
    gradient.addColorStop(1, 'rgba(139, 184, 255, 0.7)');

    new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: dados.maquinas_labels,
            datasets: [{
                label: 'Utilizações',
                data: dados.maquinas_dados,
                backgroundColor: gradient,
                borderColor: CORES.azul,
                borderWidth: 0,
                borderRadius: 8,
                borderSkipped: false,
                barThickness: 14
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            var v = context.parsed.x;
                            return ' ' + v + (v === 1 ? ' utilização' : ' utilizações');
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: { stepSize: 1, precision: 0, color: '#9ca3af' },
                    grid: { color: 'rgba(229, 231, 235, 0.6)', drawBorder: false }
                },
                y: {
                    ticks: { font: { size: 12, weight: '600' }, color: '#374151' },
                    grid: { display: false }
                }
            }
        }
    });
}