document.getElementById("butao").addEventListener("click", function () {
    // Captura os valores dos campos do formulário
    const cpfPaciente = document.getElementById("cpfPaciente").value;
    const sexo = document.getElementById("sexo").value;
    const data = document.getElementById("data").value;
    const email = document.getElementById("email").value;
    const telefone = document.getElementById("telefone").value;
    const crmMedico = document.getElementById("nomeMed").value;
    const especialidade = document.getElementById("especialidade").value;

    // Limpa mensagens anteriores
    document.getElementById("mensagem").innerText = "";
    document.getElementById("erro").innerText = "";

    // Validação simples
    if (!cpfPaciente || !sexo || !data || !email || !telefone || !crmMedico || !especialidade) {
        document.getElementById("erro").innerText = "Por favor, preencha todos os campos!";
        return;
    }

    // Cria o objeto JSON com os dados do formulário
    const agendamento = {
        cpfPaciente: cpfPaciente,
        sexo: sexo,
        data: data,
        email: email,
        telefone: telefone,
        crmMedico: crmMedico,
        especialidade: especialidade
    };

    // Envia os dados para a API FastAPI usando Fetch API
    fetch("http://localhost:8000/agendar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(agendamento), // Converte o objeto JS para JSON
    })
    .then(response => response.json()) // Trata a resposta da API
    .then(data => {
        // Exibe uma mensagem de sucesso ou de erro
        if (data.success) {
            document.getElementById("mensagem").innerText = "Agendamento realizado com sucesso!";
        } else {
            document.getElementById("erro").innerText = "Erro ao realizar o agendamento. Tente novamente.";
        }
    })
    .catch((error) => {
        console.error("Erro:", error);
        document.getElementById("erro").innerText = "Erro ao conectar com o servidor.";
    });
});
