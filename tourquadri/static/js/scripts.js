// ========================================
// TOURQUADRI - Scripts do Sistema
// ========================================

// ========================================
// MÁSCARA DE TELEFONE
// ========================================

function formatarTelefone(valor) {
    valor = valor.replace(/\D/g, '');
    if (valor.length > 11) {
        valor = valor.slice(0, 11);
    }
    if (valor.length === 0) {
        return '';
    } else if (valor.length <= 2) {
        return '(' + valor;
    } else if (valor.length <= 6) {
        return '(' + valor.slice(0, 2) + ') ' + valor.slice(2);
    } else if (valor.length <= 10) {
        return '(' + valor.slice(0, 2) + ') ' + valor.slice(2, 6) + '-' + valor.slice(6);
    } else {
        return '(' + valor.slice(0, 2) + ') ' + valor.slice(2, 7) + '-' + valor.slice(7, 11);
    }
}

function initMascaras() {
    const camposTelefone = document.querySelectorAll('.telefone-mask');
    camposTelefone.forEach(function(campo) {
        campo.addEventListener('input', function(e) {
            var input = e.target;
            var valorDigitado = input.value;
            var estaApagando = e.inputType === 'deleteContentBackward';
            var posicaoCursor = input.selectionStart;
            var digitosAntesDoCursor = valorDigitado.substring(0, posicaoCursor).replace(/\D/g, '').length;

            if (estaApagando && digitosAntesDoCursor > 0) {
                digitosAntesDoCursor--;
            }

            var numeros = valorDigitado.replace(/\D/g, '');
            if (numeros.length > 11) {
                numeros = numeros.slice(0, 11);
            }

            var valorFormatado = formatarTelefone(numeros);
            input.value = valorFormatado;

            var novosDigitosContados = 0;
            var novaPosicao = valorFormatado.length;

            for (var i = 0; i < valorFormatado.length; i++) {
                if (/\d/.test(valorFormatado[i])) {
                    if (novosDigitosContados === digitosAntesDoCursor) {
                        novaPosicao = i;
                        break;
                    }
                    novosDigitosContados++;
                }
            }

            if (novosDigitosContados < digitosAntesDoCursor) {
                novaPosicao = valorFormatado.length;
            } else if (novosDigitosContados === digitosAntesDoCursor) {
                novaPosicao = Math.min(valorFormatado.length, novaPosicao + 1);
            }

            input.setSelectionRange(novaPosicao, novaPosicao);
        });

        campo.addEventListener('keydown', function(e) {
            if (!/^[0-9]$/.test(e.key) && 
                e.key !== 'Backspace' && 
                e.key !== 'Delete' && 
                e.key !== 'Tab' && 
                e.key !== 'ArrowLeft' && 
                e.key !== 'ArrowRight' && 
                e.key !== 'Home' && 
                e.key !== 'End' &&
                e.key !== 'Enter') {
                e.preventDefault();
            }
        });

        campo.addEventListener('blur', function() {
            var valor = this.value;
            var numeros = valor.replace(/\D/g, '');
            if (numeros.length > 0) {
                this.value = formatarTelefone(numeros);
            }
        });
    });
}

// ========================================
// VALIDAÇÃO DE SENHA FORTE
// ========================================

function validarSenhaForte(senha) {
    const erros = [];
    if (senha.length < 8) erros.push("mínimo 8 caracteres");
    if (!/[A-Z]/.test(senha)) erros.push("maiúscula");
    if (!/[a-z]/.test(senha)) erros.push("minúscula");
    if (!/[0-9]/.test(senha)) erros.push("número");
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(senha)) erros.push("especial");
    return erros;
}

// ========================================
// FUNÇÕES DE TOGGLE SENHA
// ========================================

function toggleRedefinirNovaSenha() {
    const input = document.getElementById('redefinir_nova_senha');
    const icone = document.getElementById('iconeRedefinirNovaSenha');
    if (input.type === 'password') {
        input.type = 'text';
        icone.className = 'fas fa-eye';
    } else {
        input.type = 'password';
        icone.className = 'fas fa-eye-slash';
    }
}

function toggleRedefinirConfirmarSenha() {
    const input = document.getElementById('redefinir_confirmar_senha');
    const icone = document.getElementById('iconeRedefinirConfirmarSenha');
    if (input.type === 'password') {
        input.type = 'text';
        icone.className = 'fas fa-eye';
    } else {
        input.type = 'password';
        icone.className = 'fas fa-eye-slash';
    }
}

function toggleSenhaLogin() {
    const input = document.getElementById('senhaLogin');
    const icone = document.getElementById('iconeSenhaLogin');
    if (input.type === 'password') {
        input.type = 'text';
        icone.className = 'fas fa-eye';
    } else {
        input.type = 'password';
        icone.className = 'fas fa-eye-slash';
    }
}

function toggleSenhaRegister() {
    const input = document.getElementById('senhaRegister');
    const icone = document.getElementById('iconeSenhaRegister');
    if (input.type === 'password') {
        input.type = 'text';
        icone.className = 'fas fa-eye';
    } else {
        input.type = 'password';
        icone.className = 'fas fa-eye-slash';
    }
}

function toggleConfirmarSenha() {
    const input = document.getElementById('confirmarSenhaRegister');
    const icone = document.getElementById('iconeConfirmarSenha');
    if (input.type === 'password') {
        input.type = 'text';
        icone.className = 'fas fa-eye';
    } else {
        input.type = 'password';
        icone.className = 'fas fa-eye-slash';
    }
}

function toggleSenhaAtual() {
    const input = document.getElementById('senha_atual');
    const icone = document.getElementById('iconeSenhaAtual');
    if (input.type === 'password') {
        input.type = 'text';
        icone.className = 'fas fa-eye';
    } else {
        input.type = 'password';
        icone.className = 'fas fa-eye-slash';
    }
}

function toggleNovaSenha() {
    const input = document.getElementById('nova_senha');
    const icone = document.getElementById('iconeNovaSenha');
    if (input.type === 'password') {
        input.type = 'text';
        icone.className = 'fas fa-eye';
    } else {
        input.type = 'password';
        icone.className = 'fas fa-eye-slash';
    }
}

function toggleConfirmarNovaSenha() {
    const input = document.getElementById('confirmar_senha');
    const icone = document.getElementById('iconeConfirmarNovaSenha');
    if (input.type === 'password') {
        input.type = 'text';
        icone.className = 'fas fa-eye';
    } else {
        input.type = 'password';
        icone.className = 'fas fa-eye-slash';
    }
}

// ========================================
// MODAL DE CONFIRMAÇÃO
// ========================================

var confirmacaoResolve = null;

function confirmarModal(mensagem, titulo) {
    return new Promise(function(resolve) {
        var modal = document.getElementById('modalConfirmacao');
        var tituloEl = document.getElementById('modalConfirmacaoTitulo');
        var mensagemEl = document.getElementById('modalConfirmacaoMensagem');
        var confirmarBtn = document.getElementById('modalConfirmacaoConfirmar');
        var cancelarBtn = document.getElementById('modalConfirmacaoCancelar');

        tituloEl.textContent = titulo || 'Confirmar ação';
        mensagemEl.textContent = mensagem || 'Tem certeza que deseja realizar esta ação?';

        modal.style.display = 'flex';

        function limpar() {
            modal.style.display = 'none';
            confirmarBtn.removeEventListener('click', onConfirm);
            cancelarBtn.removeEventListener('click', onCancel);
        }

        function onConfirm() {
            limpar();
            resolve(true);
        }

        function onCancel() {
            limpar();
            resolve(false);
        }

        confirmarBtn.addEventListener('click', onConfirm);
        cancelarBtn.addEventListener('click', onCancel);

        var overlay = modal.querySelector('.modal-confirmacao-overlay');
        overlay.addEventListener('click', onCancel);
    });
}

function confirmarAcaoModal(mensagem, titulo) {
    return confirmarModal(mensagem, titulo);
}

function confirmarExclusao(url, mensagem, titulo) {
    confirmarAcaoModal(mensagem, titulo).then(function(resultado) {
        if (resultado) {
            window.location.href = url;
        }
    });
}

// ========================================
// FUNÇÃO PARA REGISTER (VALIDAÇÕES)
// ========================================

function atualizarRequisitosSenha(senha) {
    const requisitos = {
        comprimento: senha.length >= 8,
        maiuscula: /[A-Z]/.test(senha),
        minuscula: /[a-z]/.test(senha),
        numero: /[0-9]/.test(senha),
        especial: /[!@#$%^&*(),.?":{}|<>]/.test(senha)
    };

    const elementos = {
        comprimento: document.getElementById('req-comprimento'),
        maiuscula: document.getElementById('req-maiuscula'),
        minuscula: document.getElementById('req-minuscula'),
        numero: document.getElementById('req-numero'),
        especial: document.getElementById('req-especial')
    };

    const texto = {
        comprimento: 'Mínimo 8 caracteres',
        maiuscula: 'Pelo menos 1 letra maiúscula (A-Z)',
        minuscula: 'Pelo menos 1 letra minúscula (a-z)',
        numero: 'Pelo menos 1 número (0-9)',
        especial: 'Pelo menos 1 caractere especial (!@#$%^&*...)'
    };

    let todosOk = true;

    for (const [key, ok] of Object.entries(requisitos)) {
        const el = elementos[key];
        if (el) {
            if (ok) {
                el.innerHTML = '✅ ' + texto[key];
                el.style.color = '#16a34a';
            } else {
                el.innerHTML = '❌ ' + texto[key];
                el.style.color = '#dc2626';
                todosOk = false;
            }
        }
    }

    return todosOk;
}

function inicializarRegister() {
    const form = document.getElementById('form-register');
    const nome = document.getElementById('nome');
    const telefone = document.getElementById('telefone');
    const email = document.getElementById('email');
    const senha = document.getElementById('senhaRegister');
    const confirmar = document.getElementById('confirmarSenhaRegister');

    const nomeErro = document.getElementById('nome-erro');
    const telefoneErro = document.getElementById('telefone-erro');
    const emailErro = document.getElementById('email-erro');
    const confirmarErro = document.getElementById('confirmar-erro');

    if (!form) return;

    if (nome) {
        nome.addEventListener('input', function() {
            if (this.value.length > 0 && this.value.length < 3) {
                nomeErro.style.display = 'block';
                this.classList.add('campo-erro');
            } else {
                nomeErro.style.display = 'none';
                this.classList.remove('campo-erro');
            }
        });
    }

    if (telefone) {
        telefone.addEventListener('input', function() {
            this.value = this.value.replace(/\D/g, '');
            if (this.value.length > 11) {
                this.value = this.value.slice(0, 11);
            }
            if (this.value.length > 0 && this.value.length < 10) {
                telefoneErro.style.display = 'block';
                this.classList.add('campo-erro');
            } else if (this.value.length >= 10) {
                telefoneErro.style.display = 'none';
                this.classList.remove('campo-erro');
            } else {
                telefoneErro.style.display = 'none';
                this.classList.remove('campo-erro');
            }
        });
        telefone.addEventListener('keydown', function(e) {
            if (!/^[0-9]$/.test(e.key) && 
                e.key !== 'Backspace' && 
                e.key !== 'Delete' && 
                e.key !== 'Tab' && 
                e.key !== 'ArrowLeft' && 
                e.key !== 'ArrowRight' && 
                e.key !== 'Home' && 
                e.key !== 'End' &&
                e.key !== 'Enter') {
                e.preventDefault();
            }
        });
    }

    if (email) {
        email.addEventListener('input', function() {
            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (this.value.length > 0 && !emailRegex.test(this.value)) {
                emailErro.style.display = 'block';
                this.classList.add('campo-erro');
            } else {
                emailErro.style.display = 'none';
                this.classList.remove('campo-erro');
            }
        });
    }

    if (senha) {
        senha.addEventListener('input', function() {
            const requisitosDiv = document.getElementById('senha-requisitos');
            const senhaOk = atualizarRequisitosSenha(this.value);

            if (this.value.length > 0) {
                requisitosDiv.style.display = 'block';
                if (senhaOk) {
                    this.classList.remove('campo-erro');
                } else {
                    this.classList.add('campo-erro');
                }
            } else {
                requisitosDiv.style.display = 'none';
                this.classList.remove('campo-erro');
            }
            validarConfirmacaoRegister();
        });
    }

    function validarConfirmacaoRegister() {
        if (!confirmar) return;
        if (confirmar.value.length > 0) {
            if (confirmar.value !== senha.value) {
                confirmarErro.style.display = 'block';
                confirmar.classList.add('campo-erro');
            } else {
                confirmarErro.style.display = 'none';
                confirmar.classList.remove('campo-erro');
            }
        } else {
            confirmarErro.style.display = 'none';
            confirmar.classList.remove('campo-erro');
        }
    }

    if (confirmar) {
        confirmar.addEventListener('input', validarConfirmacaoRegister);
    }

    if (form) {
        form.addEventListener('submit', function(e) {
            let temErro = false;

            document.querySelectorAll('.campo-erro').forEach(function(el) {
                el.classList.remove('campo-erro');
            });

            if (nome && nome.value.length < 3) {
                nomeErro.style.display = 'block';
                nome.classList.add('campo-erro');
                temErro = true;
            }

            if (telefone) {
                const telNumeros = telefone.value.replace(/\D/g, '');
                if (telNumeros.length < 10 || telNumeros.length > 11) {
                    telefoneErro.style.display = 'block';
                    telefone.classList.add('campo-erro');
                    temErro = true;
                }
            }

            if (email) {
                const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
                if (!emailRegex.test(email.value)) {
                    emailErro.style.display = 'block';
                    email.classList.add('campo-erro');
                    temErro = true;
                }
            }

            if (senha && !atualizarRequisitosSenha(senha.value)) {
                senha.classList.add('campo-erro');
                temErro = true;
            }

            if (confirmar && confirmar.value !== senha.value) {
                confirmarErro.style.display = 'block';
                confirmar.classList.add('campo-erro');
                temErro = true;
            }

            if (temErro) {
                e.preventDefault();
                const primeiroErro = document.querySelector('.campo-erro');
                if (primeiroErro) {
                    primeiroErro.focus();
                }
            }
        });
    }
}

// ========================================
// FUNÇÃO PARA ALTERAR SENHA
// ========================================

function atualizarRequisitosAlterar(senha) {
    const requisitos = {
        comprimento: senha.length >= 8,
        maiuscula: /[A-Z]/.test(senha),
        minuscula: /[a-z]/.test(senha),
        numero: /[0-9]/.test(senha),
        especial: /[!@#$%^&*(),.?":{}|<>]/.test(senha)
    };

    const elementos = {
        comprimento: document.getElementById('req-alt-comprimento'),
        maiuscula: document.getElementById('req-alt-maiuscula'),
        minuscula: document.getElementById('req-alt-minuscula'),
        numero: document.getElementById('req-alt-numero'),
        especial: document.getElementById('req-alt-especial')
    };

    const texto = {
        comprimento: 'Mínimo 8 caracteres',
        maiuscula: 'Pelo menos 1 letra maiúscula (A-Z)',
        minuscula: 'Pelo menos 1 letra minúscula (a-z)',
        numero: 'Pelo menos 1 número (0-9)',
        especial: 'Pelo menos 1 caractere especial (!@#$%^&*...)'
    };

    let todosOk = true;

    for (const [key, ok] of Object.entries(requisitos)) {
        const el = elementos[key];
        if (el) {
            if (ok) {
                el.innerHTML = '✅ ' + texto[key];
                el.style.color = '#16a34a';
            } else {
                el.innerHTML = '❌ ' + texto[key];
                el.style.color = '#dc2626';
                todosOk = false;
            }
        }
    }

    return todosOk;
}

function inicializarAlterarSenha() {
    const form = document.getElementById('form-alterar-senha');
    const novaSenha = document.getElementById('nova_senha');
    const confirmarSenha = document.getElementById('confirmar_senha');

    if (!form) return;

    if (novaSenha) {
        novaSenha.addEventListener('input', function() {
            const requisitosDiv = document.getElementById('senha-requisitos-alterar');
            const senhaOk = atualizarRequisitosAlterar(this.value);

            if (this.value.length > 0) {
                requisitosDiv.style.display = 'block';
                if (senhaOk) {
                    this.classList.remove('campo-erro');
                } else {
                    this.classList.add('campo-erro');
                }
            } else {
                requisitosDiv.style.display = 'none';
                this.classList.remove('campo-erro');
            }
            validarConfirmacaoAlterar();
        });
    }

    function validarConfirmacaoAlterar() {
        if (!confirmarSenha) return;
        if (confirmarSenha.value.length > 0) {
            if (confirmarSenha.value !== novaSenha.value) {
                confirmarSenha.classList.add('campo-erro');
            } else {
                confirmarSenha.classList.remove('campo-erro');
            }
        } else {
            confirmarSenha.classList.remove('campo-erro');
        }
    }

    if (confirmarSenha) {
        confirmarSenha.addEventListener('input', validarConfirmacaoAlterar);
    }

    if (form) {
        form.addEventListener('submit', function(e) {
            let temErro = false;

            document.querySelectorAll('.campo-erro').forEach(function(el) {
                el.classList.remove('campo-erro');
            });

            if (!atualizarRequisitosAlterar(novaSenha.value)) {
                novaSenha.classList.add('campo-erro');
                temErro = true;
            }

            if (confirmarSenha.value !== novaSenha.value) {
                confirmarSenha.classList.add('campo-erro');
                temErro = true;
            }

            if (temErro) {
                e.preventDefault();
                const primeiroErro = document.querySelector('.campo-erro');
                if (primeiroErro) {
                    primeiroErro.focus();
                }
            }
        });
    }
}

// ========================================
// FUNÇÃO PARA REDEFINIR SENHA
// ========================================

function inicializarRedefinirSenha() {
    const form = document.getElementById('form-redefinir-senha');
    const novaSenha = document.getElementById('redefinir_nova_senha');
    const confirmarSenha = document.getElementById('redefinir_confirmar_senha');

    if (!form) return;

    if (novaSenha) {
        novaSenha.addEventListener('input', function() {
            validarConfirmacaoRedefinir();
        });
    }

    function validarConfirmacaoRedefinir() {
        if (!confirmarSenha) return;
        if (confirmarSenha.value.length > 0) {
            if (confirmarSenha.value !== novaSenha.value) {
                confirmarSenha.classList.add('campo-erro');
            } else {
                confirmarSenha.classList.remove('campo-erro');
            }
        } else {
            confirmarSenha.classList.remove('campo-erro');
        }
    }

    if (confirmarSenha) {
        confirmarSenha.addEventListener('input', validarConfirmacaoRedefinir);
    }

    if (form) {
        form.addEventListener('submit', function(e) {
            let temErro = false;

            document.querySelectorAll('.campo-erro').forEach(function(el) {
                el.classList.remove('campo-erro');
            });

            if (novaSenha.value.length < 8) {
                novaSenha.classList.add('campo-erro');
                temErro = true;
            }

            if (confirmarSenha.value !== novaSenha.value) {
                confirmarSenha.classList.add('campo-erro');
                temErro = true;
            }

            if (temErro) {
                e.preventDefault();
                const primeiroErro = document.querySelector('.campo-erro');
                if (primeiroErro) {
                    primeiroErro.focus();
                }
            }
        });
    }
}

// ========================================
// HELPER — VERIFICA DISPONIBILIDADE DE MÁQUINAS
// ========================================

function aplicarDisponibilidade(dados, maquinasCheckboxes) {
    var ocupadas = dados.ocupadas || [];

    maquinasCheckboxes.forEach(function(checkbox) {
        var maquinaNum = parseInt(checkbox.value);
        var maquinaDiv = document.getElementById('maquina-' + maquinaNum);
        if (!maquinaDiv) return;

        if (ocupadas.indexOf(maquinaNum) !== -1) {
            checkbox.disabled = true;
            checkbox.checked = false;
            maquinaDiv.classList.add('indisponivel');
            maquinaDiv.classList.remove('selecionada');
        } else {
            checkbox.disabled = false;
            maquinaDiv.classList.remove('indisponivel');
        }
    });

    var maquinasAviso = document.getElementById('maquinas-aviso');
    if (maquinasAviso) {
        maquinasAviso.style.display = (ocupadas.length > 0) ? 'block' : 'none';
    }
}

function limparDisponibilidade(maquinasCheckboxes) {
    maquinasCheckboxes.forEach(function(checkbox) {
        checkbox.disabled = false;
        var maquinaDiv = document.getElementById('maquina-' + parseInt(checkbox.value));
        if (maquinaDiv) maquinaDiv.classList.remove('indisponivel');
    });
    var maquinasAviso = document.getElementById('maquinas-aviso');
    if (maquinasAviso) maquinasAviso.style.display = 'none';
}

// ========================================
// FUNÇÃO PARA AGENDAMENTO (DASHBOARD)
// ========================================

function inicializarAgendamento() {
    var dataInput = document.getElementById('data');
    var horarioSelect = document.getElementById('horario');
    var roteiroSelect = document.getElementById('roteiro');
    var maquinasCheckboxes = document.querySelectorAll('input[name="maquinas"]');
    var nenhumaSelecionada = document.getElementById('nenhuma-selecionada');
    var btnAgendar = document.getElementById('btn-agendar');
    var form = document.getElementById('form-agendamento');

    var dataInvalidaMsg = document.getElementById('data-invalida-msg');
    var dataBloqueadaMsg = document.getElementById('data-bloqueada-msg');
    var horarioIndisponivelMsg = document.getElementById('horario-indisponivel-msg');

    var agora = new Date();
    var hoje = agora.toISOString().split('T')[0];

    var dataMinima = dataInput.getAttribute('min');
    dataInput.setAttribute('min', dataMinima);
    dataInput.value = '';

    var dataLimite = new Date(agora);
    dataLimite.setDate(dataLimite.getDate() + 30);
    dataInput.setAttribute('max', dataLimite.toISOString().split('T')[0]);

    window.toggleMaquina = function(numero) {
        var checkbox = document.getElementById('maquina-check-' + numero);
        var maquinaDiv = document.getElementById('maquina-' + numero);

        if (maquinaDiv && maquinaDiv.classList.contains('indisponivel')) return;
        if (checkbox.disabled) return;

        checkbox.checked = !checkbox.checked;
        if (checkbox.checked) {
            maquinaDiv.classList.add('selecionada');
        } else {
            maquinaDiv.classList.remove('selecionada');
        }
    };

    function desmarcarTodasMaquinas() {
        document.querySelectorAll('input[name="maquinas"]').forEach(function(c) {
            c.checked = false;
            var div = document.getElementById('maquina-' + parseInt(c.value));
            if (div) div.classList.remove('selecionada');
        });
    }

    function tentarVerificar() {
        if (!dataInput.value || !horarioSelect.value) {
            desmarcarTodasMaquinas();
            limparDisponibilidade(maquinasCheckboxes);
            return;
        }
        verificarDisponibilidade();
    }

    function atualizarHorariosDisponiveis() {
        var data = dataInput.value;
        var options = horarioSelect.querySelectorAll('option');
        var hojeStr = new Date().toISOString().split('T')[0];
        var agora = new Date();
        var horarioAtualMin = agora.getHours() * 60 + agora.getMinutes();

        if (!data) {
            options.forEach(function(o) {
                o.disabled = false;
                o.style.color = '';
                o.style.background = '';
            });
            if (dataInvalidaMsg) dataInvalidaMsg.style.display = 'none';
            if (dataBloqueadaMsg) dataBloqueadaMsg.style.display = 'none';
            if (horarioIndisponivelMsg) horarioIndisponivelMsg.style.display = 'none';
            limparDisponibilidade(maquinasCheckboxes);
            return;
        }

        var dataSelecionada = new Date(data + 'T00:00:00');
        var hojeDate = new Date();
        hojeDate.setHours(0, 0, 0, 0);

        if (dataSelecionada < hojeDate) {
            if (dataInvalidaMsg) {
                dataInvalidaMsg.style.display = 'block';
                dataInvalidaMsg.innerHTML = '<i class="fas fa-exclamation-circle"></i> Data inválida. Selecione uma data futura.';
            }
            if (dataBloqueadaMsg) dataBloqueadaMsg.style.display = 'none';
            if (horarioIndisponivelMsg) horarioIndisponivelMsg.style.display = 'none';
            options.forEach(function(o) {
                o.disabled = true;
                o.style.color = '#9ca3af';
                o.style.background = '#f3f4f6';
            });
            desmarcarTodasMaquinas();
            return;
        } else {
            if (dataInvalidaMsg) dataInvalidaMsg.style.display = 'none';
        }

        if (data === hojeStr && agora.getHours() >= 17) {
            if (dataInvalidaMsg) {
                dataInvalidaMsg.style.display = 'block';
                dataInvalidaMsg.innerHTML = '<i class="fas fa-exclamation-circle"></i> Não é possível agendar para hoje após as 17h. Selecione uma data futura.';
            }
            options.forEach(function(o) {
                o.disabled = true;
                o.style.color = '#9ca3af';
                o.style.background = '#f3f4f6';
            });
            desmarcarTodasMaquinas();
            return;
        }

        var primeiroDisponivel = null;
        options.forEach(function(option) {
            var valor = option.value;
            if (!valor) return;
            var partes = valor.split(':');
            var horarioMin = parseInt(partes[0]) * 60 + parseInt(partes[1]);
            var ehPassado = (data === hojeStr && horarioMin <= horarioAtualMin);

            if (ehPassado) {
                option.disabled = true;
                option.style.color = '#9ca3af';
                option.style.background = '#f3f4f6';
            } else {
                option.disabled = false;
                option.style.color = '';
                option.style.background = '';
                if (!primeiroDisponivel) primeiroDisponivel = valor;
            }
        });

        if (primeiroDisponivel) {
            horarioSelect.value = primeiroDisponivel;
        }

        fetch('/api/verificar_bloqueios?data=' + data)
            .then(function(r) { return r.json(); })
            .then(function(dados) {
                var bloqueados = dados.bloqueados || [];
                var todosBloqueados = dados.todos_bloqueados || false;

                if (todosBloqueados) {
                    if (dataBloqueadaMsg) dataBloqueadaMsg.style.display = 'block';
                    if (horarioIndisponivelMsg) horarioIndisponivelMsg.style.display = 'none';
                    options.forEach(function(o) {
                        o.disabled = true;
                        o.style.color = '#9ca3af';
                        o.style.background = '#f3f4f6';
                    });
                    desmarcarTodasMaquinas();
                    return;
                } else {
                    if (dataBloqueadaMsg) dataBloqueadaMsg.style.display = 'none';
                }

                if (horarioIndisponivelMsg) {
                    horarioIndisponivelMsg.style.display = (bloqueados.length > 0 && !todosBloqueados) ? 'block' : 'none';
                }

                options.forEach(function(option) {
                    var valor = option.value;
                    if (!valor) return;
                    if (bloqueados.indexOf(valor) !== -1) {
                        option.disabled = true;
                        option.style.color = '#9ca3af';
                        option.style.background = '#f3f4f6';
                    }
                });

                var primeiroDisponivelFinal = null;
                options.forEach(function(option) {
                    if (option.value && !option.disabled && !primeiroDisponivelFinal) {
                        primeiroDisponivelFinal = option.value;
                    }
                });

                if (primeiroDisponivelFinal) {
                    horarioSelect.value = primeiroDisponivelFinal;
                }

                tentarVerificar();
            })
            .catch(function(error) {
                console.error('Erro ao buscar bloqueios:', error);
            });
    }

    function verificarDisponibilidade() {
        var data = dataInput.value;
        var horario = horarioSelect.value;
        var hojeStr = new Date().toISOString().split('T')[0];
        var agora = new Date();

        if (!data || !horario) return;

        if (dataBloqueadaMsg && dataBloqueadaMsg.style.display === 'block') return;

        if (data < hojeStr || (data === hojeStr && agora.getHours() >= 17)) {
            desmarcarTodasMaquinas();
            return;
        }

        fetch('/api/verificar_maquinas?data=' + data + '&horario=' + horario + '&roteiro=' + (roteiroSelect.value || ''))
            .then(function(response) { return response.json(); })
            .then(function(dados) {
                aplicarDisponibilidade(dados, maquinasCheckboxes);
            })
            .catch(function(error) {
                console.error('Erro ao verificar disponibilidade:', error);
            });
    }

    // Eventos
    dataInput.addEventListener('change', function() {
        desmarcarTodasMaquinas();
        atualizarHorariosDisponiveis();
    });

    horarioSelect.addEventListener('change', tentarVerificar);
    roteiroSelect.addEventListener('change', tentarVerificar);

    form.addEventListener('submit', function(e) {
        var data = dataInput.value;
        var horario = horarioSelect.value;
        var selecionadas = document.querySelectorAll('input[name="maquinas"]:checked');

        var hojeStr = new Date().toISOString().split('T')[0];
        var agora = new Date();
        var horarioAtualMin = agora.getHours() * 60 + agora.getMinutes();

        var dataSelecionada = new Date(data + 'T00:00:00');
        var hojeDate = new Date();
        hojeDate.setHours(0, 0, 0, 0);

        if (dataSelecionada < hojeDate) {
            e.preventDefault();
            if (dataInvalidaMsg) {
                dataInvalidaMsg.style.display = 'block';
                dataInvalidaMsg.innerHTML = '<i class="fas fa-exclamation-circle"></i> Data inválida. Selecione uma data futura.';
            }
            return;
        }

        if (data === hojeStr && agora.getHours() >= 17) {
            e.preventDefault();
            if (dataInvalidaMsg) {
                dataInvalidaMsg.style.display = 'block';
                dataInvalidaMsg.innerHTML = '<i class="fas fa-exclamation-circle"></i> Não é possível agendar para hoje após as 17h.';
            }
            return;
        }

        if (data === hojeStr && horario) {
            var partes = horario.split(':');
            var horarioMin = parseInt(partes[0]) * 60 + parseInt(partes[1]);
            if (horarioMin <= horarioAtualMin) {
                e.preventDefault();
                return;
            }
        }

        if (selecionadas.length === 0) {
            e.preventDefault();
            if (nenhumaSelecionada) {
                nenhumaSelecionada.style.display = 'block';
                setTimeout(function() {
                    nenhumaSelecionada.style.display = 'none';
                }, 3000);
            }
            return;
        }

        btnAgendar.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Agendando...';
        btnAgendar.disabled = true;
    });

    setTimeout(function() {
        atualizarHorariosDisponiveis();
    }, 300);
}

// ========================================
// FUNÇÃO PARA EDITAR AGENDAMENTO (USUÁRIO)
// ========================================

function inicializarEditarAgendamento() {
    var dataInput = document.getElementById('data');
    var horarioSelect = document.getElementById('horario');
    var roteiroSelect = document.getElementById('roteiro');
    var maquinasCheckboxes = document.querySelectorAll('input[name="maquinas"]');
    var nenhumaSelecionada = document.getElementById('nenhuma-selecionada');
    var btnSalvar = document.getElementById('btn-salvar');
    var form = document.getElementById('form-editar');
    var agendamentoId = form ? form.getAttribute('data-agendamento-id') : '';

    var dataInvalidaMsg = document.getElementById('data-invalida-msg');
    var dataBloqueadaMsg = document.getElementById('data-bloqueada-msg');
    var horarioIndisponivelMsg = document.getElementById('horario-indisponivel-msg');

    var agora = new Date();
    var hoje = agora.toISOString().split('T')[0];

    window.toggleMaquina = function(numero) {
        var checkbox = document.getElementById('maquina-check-' + numero);
        var maquinaDiv = document.getElementById('maquina-' + numero);

        if (maquinaDiv && maquinaDiv.classList.contains('indisponivel')) return;
        if (checkbox.disabled) return;

        checkbox.checked = !checkbox.checked;
        if (checkbox.checked) {
            maquinaDiv.classList.add('selecionada');
        } else {
            maquinaDiv.classList.remove('selecionada');
        }
    };

    function desmarcarTodasMaquinas() {
        document.querySelectorAll('input[name="maquinas"]').forEach(function(c) {
            c.checked = false;
            var div = document.getElementById('maquina-' + parseInt(c.value));
            if (div) div.classList.remove('selecionada');
        });
    }

    function tentarVerificar() {
        if (!dataInput.value || !horarioSelect.value) {
            desmarcarTodasMaquinas();
            limparDisponibilidade(maquinasCheckboxes);
            return;
        }
        verificarDisponibilidade();
    }

    function atualizarHorariosDisponiveis() {
        if (!dataInput) return;
        var data = dataInput.value;
        var options = horarioSelect.querySelectorAll('option');
        var hojeStr = new Date().toISOString().split('T')[0];
        var agora = new Date();
        var horarioAtualMin = agora.getHours() * 60 + agora.getMinutes();
        var valorAtual = horarioSelect.value;

        if (!data) {
            options.forEach(function(o) {
                o.disabled = false;
                o.style.color = '';
                o.style.background = '';
            });
            if (dataInvalidaMsg) dataInvalidaMsg.style.display = 'none';
            if (dataBloqueadaMsg) dataBloqueadaMsg.style.display = 'none';
            if (horarioIndisponivelMsg) horarioIndisponivelMsg.style.display = 'none';
            limparDisponibilidade(maquinasCheckboxes);
            return;
        }

        var dataSelecionada = new Date(data + 'T00:00:00');
        var hojeDate = new Date();
        hojeDate.setHours(0, 0, 0, 0);

        if (dataSelecionada < hojeDate) {
            if (dataInvalidaMsg) {
                dataInvalidaMsg.style.display = 'block';
                dataInvalidaMsg.innerHTML = '<i class="fas fa-exclamation-circle"></i> Data inválida.';
            }
            options.forEach(function(o) {
                o.disabled = true;
                o.style.color = '#9ca3af';
                o.style.background = '#f3f4f6';
            });
            return;
        } else {
            if (dataInvalidaMsg) dataInvalidaMsg.style.display = 'none';
        }

        if (data === hojeStr && agora.getHours() >= 17) {
            if (dataInvalidaMsg) {
                dataInvalidaMsg.style.display = 'block';
                dataInvalidaMsg.innerHTML = '<i class="fas fa-exclamation-circle"></i> Não é possível agendar para hoje após as 17h.';
            }
            options.forEach(function(o) {
                o.disabled = true;
                o.style.color = '#9ca3af';
                o.style.background = '#f3f4f6';
            });
            return;
        }

        var primeiroDisponivel = null;
        options.forEach(function(option) {
            var valor = option.value;
            if (!valor) return;
            var partes = valor.split(':');
            var horarioMin = parseInt(partes[0]) * 60 + parseInt(partes[1]);
            var ehPassado = (data === hojeStr && horarioMin <= horarioAtualMin);

            if (ehPassado) {
                option.disabled = true;
                option.style.color = '#9ca3af';
                option.style.background = '#f3f4f6';
            } else {
                option.disabled = false;
                option.style.color = '';
                option.style.background = '';
                if (!primeiroDisponivel) primeiroDisponivel = valor;
            }
        });

        var optionAtual = document.querySelector('option[value="' + valorAtual + '"]');
        if (valorAtual && optionAtual && !optionAtual.disabled) {
            horarioSelect.value = valorAtual;
        } else if (primeiroDisponivel) {
            horarioSelect.value = primeiroDisponivel;
        }

        fetch('/api/verificar_bloqueios?data=' + data + '&agendamento_id=' + agendamentoId)
            .then(function(r) { return r.json(); })
            .then(function(dados) {
                var bloqueados = dados.bloqueados || [];
                var todosBloqueados = dados.todos_bloqueados || false;

                if (todosBloqueados) {
                    if (dataBloqueadaMsg) dataBloqueadaMsg.style.display = 'block';
                    options.forEach(function(o) {
                        o.disabled = true;
                        o.style.color = '#9ca3af';
                        o.style.background = '#f3f4f6';
                    });
                    return;
                } else {
                    if (dataBloqueadaMsg) dataBloqueadaMsg.style.display = 'none';
                }

                if (horarioIndisponivelMsg) {
                    horarioIndisponivelMsg.style.display = (bloqueados.length > 0 && !todosBloqueados) ? 'block' : 'none';
                }

                options.forEach(function(option) {
                    var valor = option.value;
                    if (!valor) return;
                    if (bloqueados.indexOf(valor) !== -1) {
                        option.disabled = true;
                        option.style.color = '#9ca3af';
                        option.style.background = '#f3f4f6';
                    }
                });

                var primeiroDisponivelFinal = null;
                options.forEach(function(option) {
                    if (option.value && !option.disabled && !primeiroDisponivelFinal) {
                        primeiroDisponivelFinal = option.value;
                    }
                });

                if (primeiroDisponivelFinal) {
                    horarioSelect.value = primeiroDisponivelFinal;
                }

                tentarVerificar();
            })
            .catch(function(error) {
                console.error('Erro ao buscar bloqueios:', error);
            });
    }

    function verificarDisponibilidade() {
        if (!dataInput) return;
        var data = dataInput.value;
        var horario = horarioSelect.value;
        var roteiro = roteiroSelect.value;
        var hojeStr = new Date().toISOString().split('T')[0];
        var agora = new Date();

        if (!data || !horario || !roteiro) return;
        if (dataBloqueadaMsg && dataBloqueadaMsg.style.display === 'block') return;
        if (data < hojeStr || (data === hojeStr && agora.getHours() >= 17)) {
            desmarcarTodasMaquinas();
            return;
        }

        fetch('/api/verificar_maquinas?data=' + data + '&horario=' + horario + '&roteiro=' + (roteiroSelect.value || '') + '&agendamento_id=' + agendamentoId)
            .then(function(response) { return response.json(); })
            .then(function(dados) {
                aplicarDisponibilidade(dados, maquinasCheckboxes);
            })
            .catch(function(error) {
                console.error('Erro ao verificar disponibilidade:', error);
            });
    }

    if (dataInput) {
        dataInput.addEventListener('change', function() {
            desmarcarTodasMaquinas();
            atualizarHorariosDisponiveis();
        });
    }

    if (horarioSelect) horarioSelect.addEventListener('change', tentarVerificar);
    if (roteiroSelect) roteiroSelect.addEventListener('change', tentarVerificar);

    if (btnSalvar) {
        btnSalvar.addEventListener('click', function(e) {
            e.preventDefault();
            enviarFormulario();
        });
    }

    window.enviarFormulario = function() {
        if (!dataInput) return;
        var selecionadas = document.querySelectorAll('input[name="maquinas"]:checked');

        if (selecionadas.length === 0) {
            if (nenhumaSelecionada) {
                nenhumaSelecionada.style.display = 'block';
                setTimeout(function() {
                    nenhumaSelecionada.style.display = 'none';
                }, 3000);
            }
            return;
        }

        form.submit();
    };

    setTimeout(function() {
        atualizarHorariosDisponiveis();
    }, 300);
}

// ========================================
// FUNÇÃO PARA ADMIN_EDITAR
// ========================================

function inicializarAdminEditar(agendamentoId) {
    var dataInput = document.getElementById('data');
    var horarioSelect = document.getElementById('horario');
    var roteiroSelect = document.getElementById('roteiro');
    var maquinasCheckboxes = document.querySelectorAll('input[name="maquinas"]');
    var nenhumaSelecionada = document.getElementById('nenhuma-selecionada');
    var btnSalvar = document.getElementById('btn-salvar');
    var form = document.getElementById('form-editar');
    var statusSelect = document.getElementById('status');

    var dataInvalidaMsg = document.getElementById('data-invalida-msg');
    var dataBloqueadaMsg = document.getElementById('data-bloqueada-msg');
    var horarioIndisponivelMsg = document.getElementById('horario-indisponivel-msg');

    var agora = new Date();
    var hoje = agora.toISOString().split('T')[0];

    window.toggleMaquina = function(numero) {
        var checkbox = document.getElementById('maquina-check-' + numero);
        var maquinaDiv = document.getElementById('maquina-' + numero);

        if (maquinaDiv && maquinaDiv.classList.contains('indisponivel')) return;
        if (checkbox.disabled) return;

        checkbox.checked = !checkbox.checked;
        if (checkbox.checked) {
            maquinaDiv.classList.add('selecionada');
        } else {
            maquinaDiv.classList.remove('selecionada');
        }
    };

    function desmarcarTodasMaquinas() {
        document.querySelectorAll('input[name="maquinas"]').forEach(function(c) {
            c.checked = false;
            var div = document.getElementById('maquina-' + parseInt(c.value));
            if (div) div.classList.remove('selecionada');
        });
    }

    function tentarVerificar() {
        if (!dataInput.value || !horarioSelect.value) {
            desmarcarTodasMaquinas();
            limparDisponibilidade(maquinasCheckboxes);
            return;
        }
        verificarDisponibilidade();
    }

    function atualizarCampos() {
        if (!statusSelect) return;
        var isCancelado = statusSelect.value === 'cancelado';
        var campos = ['nome_cliente', 'telefone_cliente', 'email_cliente', 'data', 'horario', 'roteiro'];

        campos.forEach(function(campoId) {
            var campo = document.getElementById(campoId);
            if (campo) campo.disabled = isCancelado;
        });

        maquinasCheckboxes.forEach(function(checkbox) {
            checkbox.disabled = isCancelado;
        });

        var infoSpans = document.querySelectorAll('.mensagem-info');
        infoSpans.forEach(function(span) {
            span.style.display = isCancelado ? 'block' : 'none';
        });

        if (btnSalvar) btnSalvar.disabled = isCancelado;
    }

    function atualizarHorariosDisponiveis() {
        var data = dataInput.value;
        var options = horarioSelect.querySelectorAll('option');
        var hojeStr = new Date().toISOString().split('T')[0];
        var agora = new Date();
        var horarioAtualMin = agora.getHours() * 60 + agora.getMinutes();
        var valorAtual = horarioSelect.value;

        if (!data) {
            options.forEach(function(o) {
                o.disabled = false;
                o.style.color = '';
                o.style.background = '';
            });
            if (dataInvalidaMsg) dataInvalidaMsg.style.display = 'none';
            if (dataBloqueadaMsg) dataBloqueadaMsg.style.display = 'none';
            if (horarioIndisponivelMsg) horarioIndisponivelMsg.style.display = 'none';
            limparDisponibilidade(maquinasCheckboxes);
            return;
        }

        var dataSelecionada = new Date(data + 'T00:00:00');
        var hojeDate = new Date();
        hojeDate.setHours(0, 0, 0, 0);

        if (dataSelecionada < hojeDate) {
            if (dataInvalidaMsg) {
                dataInvalidaMsg.style.display = 'block';
                dataInvalidaMsg.innerHTML = '<i class="fas fa-exclamation-circle"></i> Data inválida.';
            }
            options.forEach(function(o) {
                o.disabled = true;
                o.style.color = '#9ca3af';
                o.style.background = '#f3f4f6';
            });
            return;
        } else {
            if (dataInvalidaMsg) dataInvalidaMsg.style.display = 'none';
        }

        if (data === hojeStr && agora.getHours() >= 17) {
            if (dataInvalidaMsg) {
                dataInvalidaMsg.style.display = 'block';
                dataInvalidaMsg.innerHTML = '<i class="fas fa-exclamation-circle"></i> Não é possível agendar para hoje após as 17h.';
            }
            options.forEach(function(o) {
                o.disabled = true;
                o.style.color = '#9ca3af';
                o.style.background = '#f3f4f6';
            });
            return;
        }

        if (statusSelect && statusSelect.value === 'cancelado') return;

        var primeiroDisponivel = null;
        options.forEach(function(option) {
            var valor = option.value;
            if (!valor) return;
            var partes = valor.split(':');
            var horarioMin = parseInt(partes[0]) * 60 + parseInt(partes[1]);
            var ehPassado = (data === hojeStr && horarioMin <= horarioAtualMin);

            if (ehPassado) {
                option.disabled = true;
                option.style.color = '#9ca3af';
                option.style.background = '#f3f4f6';
            } else {
                option.disabled = false;
                option.style.color = '';
                option.style.background = '';
                if (!primeiroDisponivel) primeiroDisponivel = valor;
            }
        });

        var optionAtual = document.querySelector('option[value="' + valorAtual + '"]');
        if (valorAtual && optionAtual && !optionAtual.disabled) {
            horarioSelect.value = valorAtual;
        } else if (primeiroDisponivel) {
            horarioSelect.value = primeiroDisponivel;
        }

        fetch('/api/verificar_bloqueios?data=' + data + '&agendamento_id=' + agendamentoId)
            .then(function(r) { return r.json(); })
            .then(function(dados) {
                var bloqueados = dados.bloqueados || [];
                var todosBloqueados = dados.todos_bloqueados || false;

                if (todosBloqueados) {
                    if (dataBloqueadaMsg) dataBloqueadaMsg.style.display = 'block';
                    options.forEach(function(o) {
                        o.disabled = true;
                        o.style.color = '#9ca3af';
                        o.style.background = '#f3f4f6';
                    });
                    return;
                } else {
                    if (dataBloqueadaMsg) dataBloqueadaMsg.style.display = 'none';
                }

                if (horarioIndisponivelMsg) {
                    horarioIndisponivelMsg.style.display = (bloqueados.length > 0 && !todosBloqueados) ? 'block' : 'none';
                }

                options.forEach(function(option) {
                    var valor = option.value;
                    if (!valor) return;
                    if (bloqueados.indexOf(valor) !== -1) {
                        option.disabled = true;
                        option.style.color = '#9ca3af';
                        option.style.background = '#f3f4f6';
                    }
                });

                var primeiroDisponivelFinal = null;
                options.forEach(function(option) {
                    if (option.value && !option.disabled && !primeiroDisponivelFinal) {
                        primeiroDisponivelFinal = option.value;
                    }
                });

                if (primeiroDisponivelFinal) {
                    horarioSelect.value = primeiroDisponivelFinal;
                }

                tentarVerificar();
            })
            .catch(function(error) {
                console.error('Erro ao buscar bloqueios:', error);
            });
    }

    function verificarDisponibilidadeAdmin() {
        var data = dataInput.value;
        var horario = horarioSelect.value;
        var roteiro = roteiroSelect.value;
        var hojeStr = new Date().toISOString().split('T')[0];
        var agora = new Date();

        if (!data || !horario || !roteiro) return;
        if (statusSelect && statusSelect.value === 'cancelado') return;
        if (dataBloqueadaMsg && dataBloqueadaMsg.style.display === 'block') return;
        if (data < hojeStr || (data === hojeStr && agora.getHours() >= 17)) {
            desmarcarTodasMaquinas();
            return;
        }

        fetch('/api/verificar_maquinas?data=' + data + '&horario=' + horario + '&roteiro=' + (roteiroSelect.value || '') + '&agendamento_id=' + agendamentoId)
            .then(function(response) { return response.json(); })
            .then(function(dados) {
                aplicarDisponibilidade(dados, maquinasCheckboxes);
            })
            .catch(function(error) {
                console.error('Erro ao verificar disponibilidade:', error);
            });
    }

    window.enviarFormularioAdmin = function() {
        if (statusSelect && statusSelect.value === 'cancelado') return;

        var selecionadas = document.querySelectorAll('input[name="maquinas"]:checked');

        if (selecionadas.length === 0) {
            if (nenhumaSelecionada) {
                nenhumaSelecionada.style.display = 'block';
                setTimeout(function() {
                    nenhumaSelecionada.style.display = 'none';
                }, 3000);
            }
            return;
        }

        form.submit();
    };

    if (dataInput) {
        dataInput.addEventListener('change', function() {
            if (!statusSelect || statusSelect.value !== 'cancelado') {
                desmarcarTodasMaquinas();
                atualizarHorariosDisponiveis();
            }
        });
    }

    if (horarioSelect) {
        horarioSelect.addEventListener('change', function() {
            if (!statusSelect || statusSelect.value !== 'cancelado') {
                tentarVerificar();
            }
        });
    }

    if (roteiroSelect) {
        roteiroSelect.addEventListener('change', function() {
            if (!statusSelect || statusSelect.value !== 'cancelado') {
                tentarVerificar();
            }
        });
    }

    if (statusSelect) {
        statusSelect.addEventListener('change', function() {
            atualizarCampos();
            if (statusSelect.value === 'agendado') {
                atualizarHorariosDisponiveis();
                tentarVerificar();
            }
        });
    }

    atualizarCampos();

    setTimeout(function() {
        if (!statusSelect || statusSelect.value !== 'cancelado') {
            atualizarHorariosDisponiveis();
        }
    }, 300);
}

// ========================================
// FUNÇÃO PARA GERENCIAR HORÁRIOS
// ========================================

function inicializarGerenciarHorarios() {
    var dataBloqueio = document.getElementById('data_bloqueio');
    var horarioBloqueio = document.getElementById('horario_bloqueio');
    var btnBloquear = document.getElementById('btn-bloquear');
    var formBloquear = document.getElementById('form-bloquear');
    var bloqueioMsg = document.getElementById('bloqueio-msg');

    var dataLote = document.getElementById('data_lote');
    var loteMsg = document.getElementById('lote-msg');

    var hoje = dataBloqueio ? dataBloqueio.getAttribute('min') : '';
    var agora = new Date();
    var horaAtual = agora.getHours();
    var minutoAtual = agora.getMinutes();

    function isHorarioPassado(horario) {
        var partes = horario.split(':');
        var horarioMin = parseInt(partes[0]) * 60 + parseInt(partes[1]);
        var atualMin = horaAtual * 60 + minutoAtual;
        return horarioMin <= atualMin;
    }

    function atualizarHorariosDisponiveis() {
        if (!dataBloqueio) return;
        var data = dataBloqueio.value;
        var options = horarioBloqueio.querySelectorAll('option');
        var hojeStr = new Date().toISOString().split('T')[0];

        if (!data) {
            options.forEach(function(o) {
                if (o.value) {
                    o.disabled = false;
                    o.style.color = '';
                    o.style.background = '';
                }
            });
            if (bloqueioMsg) bloqueioMsg.style.display = 'none';
            return;
        }

        if (data < hojeStr) {
            if (bloqueioMsg) {
                bloqueioMsg.style.display = 'block';
                bloqueioMsg.innerHTML = '<i class="fas fa-exclamation-circle"></i> Data inválida. Selecione uma data futura.';
            }
            options.forEach(function(o) {
                if (o.value) {
                    o.disabled = true;
                    o.style.color = '#9ca3af';
                    o.style.background = '#f3f4f6';
                }
            });
            if (btnBloquear) btnBloquear.disabled = true;
            return;
        } else {
            if (bloqueioMsg) bloqueioMsg.style.display = 'none';
            if (btnBloquear) btnBloquear.disabled = false;
        }

        var primeiroDisponivel = null;
        options.forEach(function(option) {
            var valor = option.value;
            if (!valor) return;
            var ehPassado = (data === hojeStr && isHorarioPassado(valor));

            if (ehPassado) {
                option.disabled = true;
                option.style.color = '#9ca3af';
                option.style.background = '#f3f4f6';
            } else {
                option.disabled = false;
                option.style.color = '';
                option.style.background = '';
                if (!primeiroDisponivel) primeiroDisponivel = valor;
            }
        });

        if (primeiroDisponivel) {
            horarioBloqueio.value = primeiroDisponivel;
        }
    }

    if (dataBloqueio) {
        dataBloqueio.addEventListener('change', atualizarHorariosDisponiveis);
    }

    if (formBloquear) {
        formBloquear.addEventListener('submit', function(e) {
            if (!dataBloqueio) return;
            var data = dataBloqueio.value;
            var horario = horarioBloqueio.value;
            var hojeStr = new Date().toISOString().split('T')[0];

            if (data < hojeStr) {
                e.preventDefault();
                if (bloqueioMsg) {
                    bloqueioMsg.style.display = 'block';
                    bloqueioMsg.innerHTML = '<i class="fas fa-exclamation-circle"></i> Data inválida.';
                }
                return;
            }

            if (data === hojeStr && isHorarioPassado(horario)) {
                e.preventDefault();
                if (bloqueioMsg) {
                    bloqueioMsg.style.display = 'block';
                    bloqueioMsg.innerHTML = '<i class="fas fa-exclamation-circle"></i> Não é possível bloquear horários passados.';
                }
                return;
            }
        });
    }

    window.validarDataLote = function() {
        if (!dataLote) return false;
        var data = dataLote.value;
        var hojeStr = new Date().toISOString().split('T')[0];

        if (data < hojeStr) {
            if (loteMsg) {
                loteMsg.style.display = 'block';
                loteMsg.innerHTML = '<i class="fas fa-exclamation-circle"></i> Selecione uma data válida.';
            }
            return false;
        }
        if (loteMsg) loteMsg.style.display = 'none';
        return true;
    };

    if (dataLote) {
        dataLote.addEventListener('change', function() {
            var data = this.value;
            var hojeStr = new Date().toISOString().split('T')[0];
            if (data < hojeStr) {
                if (loteMsg) {
                    loteMsg.style.display = 'block';
                    loteMsg.innerHTML = '<i class="fas fa-exclamation-circle"></i> Selecione uma data válida.';
                }
            } else {
                if (loteMsg) loteMsg.style.display = 'none';
            }
        });
    }

    if (dataBloqueio) dataBloqueio.setAttribute('min', hoje);
    if (dataLote) dataLote.setAttribute('min', hoje);

    setTimeout(atualizarHorariosDisponiveis, 100);
}

// ========================================
// FUNÇÕES DE INICIALIZAÇÃO
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('TourQuadri - Sistema carregado com sucesso!');

    initMascaras();

    if (document.getElementById('form-register')) {
        inicializarRegister();
    }

    if (document.getElementById('form-alterar-senha')) {
        inicializarAlterarSenha();
    }

    if (document.getElementById('form-redefinir-senha')) {
        inicializarRedefinirSenha();
    }

    if (document.getElementById('form-agendamento')) {
        inicializarAgendamento();
    }

    if (document.getElementById('data_bloqueio')) {
        inicializarGerenciarHorarios();
    }

    if (document.getElementById('form-editar')) {
        var agendamentoId = document.getElementById('form-editar').getAttribute('data-agendamento-id') || '';
        if (agendamentoId) {
            if (window.location.pathname.includes('/admin/editar/')) {
                inicializarAdminEditar(agendamentoId);
            } else {
                inicializarEditarAgendamento();
            }
        }
    }

    window.onclick = function(event) {
        if (event.target.className === 'modal') {
            event.target.style.display = 'none';
        }
        if (event.target.className === 'modal-confirmacao-overlay') {
            var modal = document.getElementById('modalConfirmacao');
            if (modal) {
                modal.style.display = 'none';
            }
        }
    };

    const mensagens = document.querySelectorAll('.mensagem.success, .mensagem.info');
    mensagens.forEach(function(mensagem) {
        if (!mensagem.closest('.landing-wrapper')) {
            setTimeout(function() {
                mensagem.style.transition = 'opacity 0.5s';
                mensagem.style.opacity = '0';
                setTimeout(function() {
                    mensagem.remove();
                }, 500);
            }, 5000);
        }
    });
});