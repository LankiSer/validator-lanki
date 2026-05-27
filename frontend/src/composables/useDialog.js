export function useDialog() {
  function showError(message, title = 'Ошибка') {
    window.alert(`${title}\n\n${message}`)
  }

  function showWarning(message, title = 'Предупреждение') {
    window.alert(`${title}\n\n${message}`)
  }

  function showInfo(message, title = 'Информация') {
    window.alert(`${title}\n\n${message}`)
  }

  function confirmAction(message, title = 'Подтверждение') {
    return window.confirm(`${title}\n\n${message}`)
  }

  return { showError, showWarning, showInfo, confirmAction }
}
