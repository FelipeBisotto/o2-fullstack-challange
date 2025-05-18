import React from 'react';
import './page_title.css';

interface PageTitleProps {
  texto: string;
}

export default function PageTitle({ texto }: PageTitleProps) {
  return <h1 className="page-title">{texto}</h1>;
}
