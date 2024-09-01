import React from 'react';

const Version = () => {
    const now = new Date();

    const pad = (number: number) => number.toString().padStart(2, '0');

    const version = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}-${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;

    return (
        <div style={{ textAlign: 'center', marginTop: '20px', color: '#fff' }}>
            Version: {version}
        </div>
    );
};

export default Version;
