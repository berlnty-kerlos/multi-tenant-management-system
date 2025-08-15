export default function TextArea(props) {
  return (
    <textarea
      style={{ padding: '8px', margin: '4px 0', display: 'block', width: '100%' }}
      rows={6}
      {...props}
    />
  );
}
