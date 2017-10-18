FROM python:3.6

ARG BUILD_DATE
ARG VCS_REF
LABEL maintainer="thia.mdossantos@gmail.com" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="Julinho IFSC: tradutor" \
      org.label-schema.description="Tradutor JSON-MQTT" \
      org.label-schema.license="MIT" \
      org.label-schema.url="https://marvietech.com.br/" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/julinho-ifsc/Tradutor" \
      org.label-schema.vendor="Marvi•E Technologies" \
      org.label-schema.version="3.6" \
      org.label-schema.schema-version="1.0"

COPY docker-entrypoint.sh requirements.txt main.py /
RUN chmod 0755 /docker-entrypoint.sh && \
    pip install --no-cache-dir -r requirements.txt && \
    groupadd tradutor && \
    useradd -g tradutor -d /tradutor -m -s /bin/false tradutor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PYTHON_ENV production

WORKDIR "/tradutor"
USER "tradutor"
EXPOSE 3000
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["python", "/main.py"]
