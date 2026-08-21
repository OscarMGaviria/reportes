export const calculateGanttData = (circuitosData, liveProgressOverrides = null, overrideCircuitName = null) => {
  const TOTAL_MONTHS = 18;
  const TOTAL_DAYS = TOTAL_MONTHS * 30; // 540 days
  const HOY_DAY = 189; // Approx mes 6.3

  // Duraciones base teóricas en días (si estuvieran al 0%)
  const BASE_DURATIONS = {
    'CONSTRUCCIÓN DE ALCANTARILLAS': 90,
    'CONSTRUCCIÓN DE DISIPADORES': 60,
    'CONSTRUCCIÓN DE FILTRO PARA CUNETAS': 60,
    'ESTABILIZACION CON MATERIAL GRANULAR': 150,
    'CONSTRUCCIÓN DE CUNETA': 90,
    'CONSTRUCCIÓN DE BORDILLOS': 45,
    'SEÑALIZACIÓN VIAL': 30
  };

  const processedCircuits = circuitosData.map(circuito => {
    // 1. Calcular progreso actual
    const progresses = {
      'CONSTRUCCIÓN DE ALCANTARILLAS': 0,
      'CONSTRUCCIÓN DE DISIPADORES': 0,
      'CONSTRUCCIÓN DE FILTRO PARA CUNETAS': 0,
      'ESTABILIZACION CON MATERIAL GRANULAR': 0,
      'CONSTRUCCIÓN DE CUNETA': 0,
      'CONSTRUCCIÓN DE BORDILLOS': 0,
      'SEÑALIZACIÓN VIAL': 0
    };

    if (circuito.categorias) {
      circuito.categorias.forEach(cat => {
        let name = cat.nombre.trim();
        if (progresses[name] !== undefined) {
          let totalInitial = 0;
          let totalExecuted = 0;
          if (cat.actividades) {
            cat.actividades.forEach(act => {
              totalInitial += (act.cantidad_inicial || 0);
              totalExecuted += (act.cantidad_ejecutada || 0);
            });
          }
          if (totalInitial > 0) {
            progresses[name] = Math.min(1, totalExecuted / totalInitial);
          } else {
            progresses[name] = 0;
          }
        }
      });
    }

    // Aplicar progresos en vivo si coinciden con el circuito solicitado
    const cName = circuito.corredor_vial || circuito.nombre || 'Circuito Desconocido';
    if (liveProgressOverrides && overrideCircuitName === cName) {
      Object.keys(liveProgressOverrides).forEach(k => {
         if (progresses[k] !== undefined) progresses[k] = liveProgressOverrides[k];
      });
    }

    // 2. Función para calcular cadena de dependencias dada una duración ajustada
    const calculateChain = (compressionFactor = 1.0) => {
      const schedule = {};
      
      const getDur = (name) => BASE_DURATIONS[name] * compressionFactor * (1 - progresses[name]);

      // Alcantarillas (A): Arranca hoy
      let aRemStart = HOY_DAY;
      let aRemEnd = aRemStart + getDur('CONSTRUCCIÓN DE ALCANTARILLAS');
      schedule['CONSTRUCCIÓN DE ALCANTARILLAS'] = { remStart: aRemStart, remEnd: aRemEnd };

      // Disipadores (D): Arranca hoy
      let dRemStart = HOY_DAY;
      let dRemEnd = dRemStart + getDur('CONSTRUCCIÓN DE DISIPADORES');
      schedule['CONSTRUCCIÓN DE DISIPADORES'] = { remStart: dRemStart, remEnd: dRemEnd };

      // Filtros (F): SS + 15 respecto a Alcantarillas
      let fRemStart = Math.max(HOY_DAY, aRemStart + (15 * compressionFactor));
      let fRemEnd = fRemStart + getDur('CONSTRUCCIÓN DE FILTRO PARA CUNETAS');
      schedule['CONSTRUCCIÓN DE FILTRO PARA CUNETAS'] = { remStart: fRemStart, remEnd: fRemEnd };

      // Estabilizacion (E): SS respecto a Filtros con 50% de desfase (empieza a mitad de los filtros)
      let eRemStart = Math.max(HOY_DAY, fRemStart + (getDur('CONSTRUCCIÓN DE FILTRO PARA CUNETAS') / 2));
      let eRemEnd = eRemStart + getDur('ESTABILIZACION CON MATERIAL GRANULAR');
      schedule['ESTABILIZACION CON MATERIAL GRANULAR'] = { remStart: eRemStart, remEnd: eRemEnd };

      // Cuneta (C): FS respecto a Estabilizacion
      let cRemStart = Math.max(HOY_DAY, eRemEnd);
      let cRemEnd = cRemStart + getDur('CONSTRUCCIÓN DE CUNETA');
      schedule['CONSTRUCCIÓN DE CUNETA'] = { remStart: cRemStart, remEnd: cRemEnd };

      // Bordillos (B): SS respecto a Cuneta (comienzan al mismo tiempo)
      let bRemStart = cRemStart; // Ahora arrancan simultáneamente
      let bRemEnd = bRemStart + getDur('CONSTRUCCIÓN DE BORDILLOS');
      schedule['CONSTRUCCIÓN DE BORDILLOS'] = { remStart: bRemStart, remEnd: bRemEnd };

      // Señalizacion (S): FS respecto a Cuneta y Estabilizacion (el que termine de último)
      let sRemStart = Math.max(HOY_DAY, eRemEnd, cRemEnd, bRemEnd);
      let sRemEnd = sRemStart + getDur('SEÑALIZACIÓN VIAL');
      schedule['SEÑALIZACIÓN VIAL'] = { remStart: sRemStart, remEnd: sRemEnd };

      return { schedule, maxEnd: sRemEnd };
    };

    // 3. Evaluar si la cadena natural excede el plazo
    let { schedule, maxEnd } = calculateChain(1.0);

    // 4. Comprimir si excede 540
    if (maxEnd > TOTAL_DAYS) {
      const requiredFactor = (TOTAL_DAYS - HOY_DAY) / (maxEnd - HOY_DAY);
      const compressed = calculateChain(requiredFactor);
      schedule = compressed.schedule;
    }

    // 5. Construir array de fases para el Gantt (cápsula visual)
    const phaseNames = [
      'CONSTRUCCIÓN DE ALCANTARILLAS',
      'CONSTRUCCIÓN DE DISIPADORES',
      'CONSTRUCCIÓN DE FILTRO PARA CUNETAS',
      'ESTABILIZACION CON MATERIAL GRANULAR',
      'CONSTRUCCIÓN DE CUNETA',
      'CONSTRUCCIÓN DE BORDILLOS',
      'SEÑALIZACIÓN VIAL'
    ];

    const fases = phaseNames.map((name, index) => {
      const p = progresses[name];
      const sched = schedule[name];
      let startDay, endDay;

      if (p === 1) {
        // 100% terminado -> En el pasado
        endDay = HOY_DAY;
        startDay = HOY_DAY - BASE_DURATIONS[name];
      } else if (p === 0) {
        // 0% -> Todo en el futuro
        startDay = sched.remStart;
        endDay = sched.remEnd;
      } else {
        // Parcial -> El final del progreso verde DEBE tocar HOY_DAY
        const remDur = sched.remEnd - sched.remStart;
        const totalDurVisual = remDur / (1 - p);
        startDay = sched.remStart - (totalDurVisual * p);
        endDay = sched.remEnd;
      }

      return {
        id: index + 1,
        name: name,
        startDay: startDay,
        endDay: endDay,
        progress: Math.round(p * 100)
      };
    });

    return {
      nombre: circuito.corredor_vial || circuito.nombre || 'Circuito Desconocido',
      fases: fases
    };
  });

  return processedCircuits;
};
